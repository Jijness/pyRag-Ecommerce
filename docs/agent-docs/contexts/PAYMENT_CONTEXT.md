# Payment Context — Thiết Kế Chi Tiết

**Service:** `payment_service` | **Port:** 8005 | **Database:** `payment_db`

---

## 1. Mô Tả Bounded Context

Payment Context bọc gói toàn bộ vòng đời của một giao dịch tài chính. Đây là **màng lọc cách ly lỗi**: nếu cổng thanh toán gặp sự cố, lỗi bị giam lỏng hoàn toàn bên trong Payment Context — các luồng duyệt sản phẩm và thêm giỏ hàng không bị ảnh hưởng.

**Thiết kế thanh toán:**
- **COD** (Cash On Delivery): Tạo Payment record với method=COD, status=PENDING → chuyển PAID khi tài xế xác nhận thu tiền
- **Online (Giả lập)**: Giao diện hiển thị nút "Thanh toán thành công" / "Thanh toán thất bại" — hệ thống gọi API tương ứng → Payment Service phát event RabbitMQ

**Actors ngoài hệ thống:**
- **Payment Gateway (giả lập)**: Trong thực tế là Momo/VNPay/PayOS. Trong assignment này được giả lập qua API endpoint nội bộ.

---

## 2. Actors & Use Cases

### Actors:
- **Customer** — Khách hàng thực hiện thanh toán
- **Staff / Admin** — Xem lịch sử giao dịch
- **Order Service** — Gửi event `order.created` để kích hoạt Payment
- **Payment Gateway (External/Simulated)** — Gửi kết quả thanh toán

### Use Case Tổng Quan:
```
[Payment Context]
    │
    ├── UC01: Khởi tạo Payment khi đặt hàng ─── Order Service
    ├── UC02: Xem trạng thái thanh toán ─────── Customer
    ├── UC03: Thanh toán Online ────────────── Customer
    │         (luồng thành công / luồng thất bại)
    ├── UC04: Xác nhận thu tiền COD ─────────── Shipping Service (sau giao hàng)
    ├── UC05: Yêu cầu hoàn tiền ─────────────── Customer
    ├── UC06: Duyệt hoàn tiền ───────────────── Admin
    ├── UC07: Xem lịch sử giao dịch ─────────── Staff, Admin
    └── UC08: Thanh toán bằng Gift Card ─────── Customer
```

| UC | Tên | Actor | Mô tả ngắn |
|---|---|---|---|
| UC01 | Khởi tạo | Order Service | Consume event `order.created` → tạo Payment (PENDING) |
| UC02 | Xem trạng thái | Customer | Xem Payment status của đơn hàng |
| UC03 | Thanh toán Online | Customer | Thực hiện thanh toán online (giả lập PayOS/Momo/VietQR). **Luồng chính:** Thanh toán thành công → payment.completed. **Luồng thay thế:** Người dùng hủy hoặc lỗi → payment.failed |
| UC04 | Thu tiền COD | Shipping Service | Sau giao DELIVERED → Payment.status = COD_PAID |
| UC05 | Yêu cầu refund | Customer | Tạo Refund request |
| UC06 | Duyệt refund | Admin | Approve/Reject Refund |
| UC07 | Lịch sử GD | Staff/Admin | Xem TransactionLog |
| UC08 | Gift Card | Customer | Dùng GiftCard để thanh toán một phần/toàn bộ |

---

## 3. Entities & Attributes

### 3.1 `Payment` — Aggregate Root
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| order_id | int | Soft ref → Order (KHÔNG dùng FK vật lý) |
| customer_id | int | Soft ref → User |
| amount | float | Số tiền cần thanh toán (snapshot từ Order) |
| currency | string | "VND" |
| method_type | string | `online` / `cod` / `gift_card` |
| status | string | PENDING / SUCCESS / FAILED / REFUNDED / COD_PAID |
| gateway_ref | string (nullable) | Mã tham chiếu từ cổng thanh toán (giả lập) |
| created_at | datetime | |
| paid_at | datetime (nullable) | Thời điểm thanh toán thành công |

### 3.2 `TransactionLog` — Entity (thuộc Payment Aggregate)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| payment_id | int (FK → Payment) | |
| event_type | string | INITIATED / CONFIRMED / FAILED / REFUNDED |
| gateway_transaction_id | string (nullable) | Mã giao dịch từ gateway |
| response_code | string | HTTP/business code từ gateway |
| response_message | text | |
| logged_at | datetime | |

### 3.3 `PaymentMethod` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| name | string | "Thanh toán khi nhận hàng", "Thẻ ngân hàng (giả lập)" |
| method_type | string | `online` / `cod` / `gift_card` |
| provider | string | "SIMULATED", "COD_PROVIDER" |
| is_active | boolean | |

### 3.4 `Refund` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| payment_id | int (FK → Payment) | |
| order_id | int | Soft ref |
| amount | float | |
| reason | text | |
| status | string | REQUESTED / APPROVED / COMPLETED / REJECTED |
| requested_at | datetime | |
| resolved_at | datetime (nullable) | |
| resolved_by | int (nullable) | Admin user_id |

### 3.5 `GiftCard` — Entity (từ interaction_service)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| code | string (unique) | |
| amount | float | Mệnh giá gốc |
| remaining_amount | float | Số tiền còn lại |
| issued_to | int (nullable) | Soft ref → Customer |
| is_active | boolean | |
| expires_at | datetime (nullable) | |

---

## 4. Relationships

| Quan hệ | Từ | Đến | Loại | Cardinality |
|---|---|---|---|---|
| Composition | Payment | TransactionLog | has-parts (cascade delete) | 1..1 → 0..* |
| Composition | Payment | Refund | has-parts | 1..1 → 0..1 |
| Association | Payment | PaymentMethod | references | 0..* → 1..1 |
| Association (Logical) | Payment | Order (Order Context) | by ID | 0..* → 1..1 |
| Association (Logical) | Payment | Customer (User Context) | by ID | 0..* → 1..1 |

---

## 5. Luồng Hoạt Động Cơ Bản

### Flow UC01: Khởi tạo Payment (consume RabbitMQ)
```
[RabbitMQ] order.created event received
  1. Parse: order_id, amount, payment_method, customer_id
  2. Tạo Payment(status=PENDING, method_type=...)
  3. Tạo TransactionLog(event_type=INITIATED)
  4. Nếu method_type = 'cod':
       Không cần chờ xác nhận → publish payment.completed (COD mode)
  5. Nếu method_type = 'online':
       Giữ status=PENDING, chờ customer xác nhận qua API
```

### Flow UC03: Thanh toán Online (giả lập)
```
Customer → POST /payments/{order_id}/confirm
  1. Tìm Payment của order_id (status=PENDING)
  2. Cập nhật:
     Payment.status = SUCCESS
     Payment.paid_at = now()
     Payment.gateway_ref = "SIMULATED_TXN_" + uuid
  3. Tạo TransactionLog(event_type=CONFIRMED)
  4. Publish event "payment.completed" → RabbitMQ
     → Order Service consume → update saga_status
     → Shipping Service consume → activate shipment

Customer → POST /payments/{order_id}/fail (giả lập thất bại)
  1. Payment.status = FAILED
  2. Tạo TransactionLog(event_type=FAILED)
  3. Publish event "payment.failed" → RabbitMQ
     → Order Service: saga compensation → COMPENSATED
```

### Flow UC05: Thu tiền COD
```
[RabbitMQ] shipment.status_changed {status: DELIVERED}
  1. Tìm Payment của order_id (method_type=COD)
  2. Payment.status = COD_PAID
  3. Payment.paid_at = now()
  4. Tạo TransactionLog(event_type=CONFIRMED)
  5. Publish "payment.completed" → Order Service
```

### Flow UC09: Gift Card
```
Customer → POST /payments/{order_id}/gift-card
  Body: { gift_card_code: "GC2026ABC" }
  1. Tìm GiftCard theo code
  2. Kiểm tra: is_active, remaining_amount > 0
  3. Nếu remaining_amount ≥ payment.amount:
       GiftCard.remaining_amount -= payment.amount
       Payment.status = SUCCESS
  4. Nếu remaining_amount < payment.amount:
       Thanh toán một phần (cần bổ sung phần còn lại)
```

---

## 6. API Endpoints Chính

| Method | Endpoint | Actor | Mô tả |
|---|---|---|---|
| GET | `/payments/{order_id}` | Customer | Xem trạng thái thanh toán |
| POST | `/payments/{order_id}/confirm` | Customer | Xác nhận thanh toán (simulate) |
| POST | `/payments/{order_id}/fail` | Customer | Thất bại thanh toán (simulate) |
| POST | `/payments/{order_id}/gift-card` | Customer | Dùng Gift Card |
| POST | `/payments/{id}/refund` | Customer | Yêu cầu hoàn tiền |
| PATCH | `/payments/refunds/{id}` | Admin | Duyệt/từ chối refund |
| GET | `/payments/transactions` | Staff/Admin | Lịch sử giao dịch |
| GET | `/payment-methods` | Customer | Xem phương thức thanh toán |

---

## 7. Django Apps Nội Bộ

```
payment_service/
├── payments/     ← Payment, TransactionLog, Refund + views
├── methods/      ← PaymentMethod
└── giftcards/    ← GiftCard
```

## 8. Ghi Chú Migration

- Source: `order_service/payment/` app
- Thêm: `TransactionLog`, `Refund`, `PaymentMethod` (models mới)
- Di chuyển: `GiftCard` từ `interaction_service`
- Tạo database mới: `payment_db`
