# Order Context — Thiết Kế Chi Tiết

**Service:** `order_service` | **Port:** 8004 | **Database:** `order_db`

---

## 1. Mô Tả Bounded Context

Order Context là **bộ điều phối giao dịch trung tâm** của hệ thống. Khi khách hàng chốt đơn, Order Context đóng vai trò Saga Orchestrator — điều phối tuần tự các bước liên quan đến Payment và Shipping thông qua RabbitMQ, đảm bảo tính nhất quán dữ liệu phân tán mà không cần distributed transaction (2PC).

**Nguyên tắc cốt lõi:**
- Order **chỉ lưu ID** (customer_id, product_id) — không sao chép dữ liệu chi tiết từ service khác
- Giá sản phẩm (`OrderItem.price`) được **snapshot tại thời điểm chốt đơn** để bảo toàn lịch sử
- Saga là **luồng nội bộ của Order Service** — các bước được xử lý qua RabbitMQ events

---

## 2. Actors & Use Cases

### Actors:
- **Customer** — Khách hàng đặt hàng
- **Staff / Admin** — Xem và quản lý đơn hàng
- **Payment Service** — Gửi event khi thanh toán thành công/thất bại
- **Shipping Service** — Gửi event khi trạng thái vận chuyển thay đổi

### Use Case Tổng Quan:
```
[Order Context]
    │
    ├── UC01: Xem lịch sử đơn hàng ──────────── Customer
    ├── UC02: Xem chi tiết đơn hàng ─────────── Customer, Staff
    ├── UC03: Đặt hàng (Checkout) ───────────── Customer
    ├── UC04: Hủy đơn hàng ─────────────────── Customer (trước khi xử lý)
    ├── UC05: Áp mã Voucher vào đơn ─────────── Customer
    ├── UC06: Xem tất cả đơn hàng (Staff) ──── Staff, Admin
    ├── UC07: Cập nhật trạng thái đơn ──────── Staff, Admin
    ├── UC08: Nhận event Payment thành công ─── Payment Service
    ├── UC09: Nhận event Payment thất bại ───── Payment Service
    └── UC10: Nhận event Shipment cập nhật ──── Shipping Service
```

| UC | Tên | Actor | Mô tả ngắn |
|---|---|---|---|
| UC01 | Lịch sử đơn | Customer | Xem danh sách đơn đã đặt, lọc theo status |
| UC02 | Chi tiết đơn | Customer/Staff | Xem đầy đủ items, giá, trạng thái, saga_status |
| UC03 | Checkout | Customer | Tạo Order từ Cart → kích hoạt Saga |
| UC04 | Hủy đơn | Customer | Chỉ hủy được khi status = PENDING |
| UC05 | Áp Voucher | Customer | Kiểm tra hợp lệ + tính discount_amount |
| UC06 | Xem tất cả | Staff/Admin | Dashboard đơn hàng, lọc/tìm kiếm |
| UC07 | Cập nhật status | Staff/Admin | APPROVE / REJECT đơn hàng |
| UC08 | Payment OK | Payment Service | Nhận event → cập nhật saga_status |
| UC09 | Payment Fail | Payment Service | Nhận event → kích hoạt Compensation |
| UC10 | Shipment update | Shipping Service | Nhận event → cập nhật order status |

---

## 3. Entities & Attributes

### 3.1 `Order` — Aggregate Root
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_id | int | Soft ref → User |
| staff_id | int (nullable) | Soft ref → Staff (được giao phụ trách) |
| status | string | PENDING / APPROVED / SHIPPING / COMPLETED / CANCELLED / REJECTED |
| subtotal | float | Tổng tiền hàng trước giảm giá |
| discount_amount | float | Số tiền giảm |
| total_price | float | Số tiền cuối cùng = subtotal - discount |
| total_quantity | int | |
| note | text | Ghi chú của khách |
| date | datetime | |
| saga_status | string | INITIATED / PAYMENT_PENDING / PAYMENT_RESERVED / SHIPPING_CREATED / CONFIRMED / PAYMENT_FAILED / COMPENSATED |
| saga_step | string | Bước saga hiện tại |
| saga_error | text | Lỗi nếu Saga thất bại |

### 3.2 `OrderItem` — Entity (thuộc Order Aggregate)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| order_id | int (FK → Order) | |
| product_id | int | Soft ref → Product |
| product_title | string | **Snapshot** tên SP lúc đặt hàng |
| price | float | **Snapshot** giá lúc đặt hàng |
| quantity | int | |

### 3.3 `Voucher` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| code | string (unique) | Mã nhập tay |
| discount_percent | float | nullable |
| discount_amount | float | nullable (fixed discount) |
| min_order_value | float | Giá trị đơn tối thiểu để áp |
| max_uses | int | nullable = unlimited |
| used_count | int | |
| valid_from | datetime | |
| valid_to | datetime | |
| is_active | boolean | |

### 3.4 `OrderDiscount` — Entity (vết lưu mã giảm đã dùng)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| order_id | int (FK → Order) | |
| voucher_code | string | Soft ref → Voucher |
| discount_applied | float | Số tiền thực tế được giảm |

---

## 4. Relationships

| Quan hệ | Từ | Đến | Loại | Cardinality |
|---|---|---|---|---|
| Composition | Order | OrderItem | has-parts (cascade delete) | 1..1 → 1..* |
| Composition | Order | OrderDiscount | has-parts (cascade delete) | 1..1 → 0..* |
| Association | OrderDiscount | Voucher | references | 0..* → 1..1 |
| Association (Logical) | Order | Customer (User Context) | by ID | 0..* → 1..1 |
| Association (Logical) | OrderItem | Product (Product Context) | by ID | 0..* → 1..1 |

---

## 5. Saga Orchestration — Luồng Đặt Hàng

### Flow Online Payment (RabbitMQ Saga):
```
Customer → POST /orders/checkout
  1. Lấy CartItems từ Cart Service (REST)
  2. Lấy giá/stock từ Product Service (REST)
  3. Tạo Order (status=PENDING, saga_status=INITIATED)
  4. Tạo OrderItems (snapshot price)
  5. Deactivate Cart (REST → Cart Service)
  6. Publish event "order.created" → RabbitMQ
     → Payment Service consume → tạo Payment (PENDING)
     → Shipping Service consume → chuẩn bị Shipment (AWAITING_PAYMENT)

  [Payment Service xử lý...]
  → Publish "payment.completed" → Order Service consume:
     saga_status = PAYMENT_RESERVED
     Publish "shipment.activate" → Shipping Service:
       → Shipment.status = PROCESSING
     Order.status = APPROVED, saga_status = CONFIRMED

  [Compensation - nếu Payment Failed]:
  → Publish "payment.failed" → Order Service consume:
     saga_status = PAYMENT_FAILED
     Order.status = CANCELLED, saga_status = COMPENSATED
     Publish "inventory.release" → Product Service (nhả stock)
```

### Flow COD (Cash On Delivery):
```
Customer → POST /orders/checkout (payment_method=COD)
  1-5. Tương tự online (tạo Order, deactivate Cart)
  6. Publish "order.created" {payment_method: "COD"}
     → Shipping Service: tạo Shipment ngay (không chờ payment)
     → Order.status = APPROVED, saga_status = CONFIRMED

  [Tài xế giao hàng...]
  → Shipping Service publish "shipment.status_changed" {status: DELIVERED}
  → Order Service consume → Order.status = COMPLETED

  [Thu tiền mặt khi giao]:
  → Payment Service publish "cod.collected"
  → Order.payment_status = PAID (COD)
```

### Saga States:
```
INITIATED
    ↓ (order.created published)
PAYMENT_PENDING ─────────── [Timeout/Error] → PAYMENT_FAILED → COMPENSATED
    ↓ (payment.completed)
PAYMENT_RESERVED
    ↓ (shipment created)
SHIPPING_CREATED
    ↓ (delivery confirmed)
CONFIRMED
```

---

## 6. Flow UC05: Áp Voucher
```
Customer → POST /orders/{id}/apply-voucher
  Body: { voucher_code: "SUMMER20" }

  1. Tìm Voucher theo code
  2. Kiểm tra:
     - is_active = True
     - valid_from ≤ now ≤ valid_to
     - used_count < max_uses (nếu có giới hạn)
     - Order.subtotal ≥ min_order_value
  3. Tính discount_amount
  4. Tạo OrderDiscount record
  5. Cập nhật Order.discount_amount + total_price
  6. Tăng Voucher.used_count
```

---

## 7. API Endpoints Chính

| Method | Endpoint | Actor | Mô tả |
|---|---|---|---|
| POST | `/orders/checkout` | Customer | Đặt hàng từ giỏ |
| GET | `/orders/` | Customer | Lịch sử đơn của mình |
| GET | `/orders/{id}` | Customer/Staff | Chi tiết đơn |
| POST | `/orders/{id}/cancel` | Customer | Hủy đơn (PENDING only) |
| POST | `/orders/{id}/apply-voucher` | Customer | Áp mã giảm giá |
| GET | `/orders/manage/` | Staff/Admin | Tất cả đơn (dashboard) |
| PATCH | `/orders/manage/{id}/status` | Staff/Admin | Cập nhật trạng thái |
| GET | `/vouchers/validate/{code}` | Customer | Kiểm tra mã hợp lệ |

---

## 8. RabbitMQ Events

| Event | Publish | Subscribe |
|---|---|---|
| `order.created` | order_service | payment_service, shipping_service |
| `payment.completed` | payment_service | order_service |
| `payment.failed` | payment_service | order_service |
| `shipment.status_changed` | shipping_service | order_service |

---

## 9. Django Apps Nội Bộ

```
order_service/
├── orders/     ← Order, OrderItem models + checkout views + saga handler
└── vouchers/   ← Voucher, OrderDiscount
```

## 10. Ghi Chú Migration

- Source: `order_service/orders/` app (giữ lại)
- Bỏ: `cart/`, `payment/`, `shipping/` apps (tách ra service riêng)
- Thêm: `vouchers/` app (từ `marketing_service.Coupon`)
- Đổi `OrderItem.book_id` → `product_id`, `book_title` → `product_title`
- Port: 8003 → **8004** (do cart_service chiếm 8003)
