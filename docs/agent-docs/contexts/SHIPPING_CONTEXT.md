# Shipping Context — Thiết Kế Chi Tiết

**Service:** `shipping_service` | **Port:** 8006 | **Database:** `shipping_db`

---

## 1. Mô Tả Bounded Context

Shipping Context tách biệt hoàn toàn miền vận chuyển khỏi miền đơn hàng vì **sự khác biệt về vòng đời dữ liệu**. Nghiệp vụ Order kết thúc khi xác nhận thanh toán thành công, trong khi Shipping tiếp tục theo dõi luồng luân chuyển hàng hóa vật lý dài ngày (PROCESSING → SHIPPING → DELIVERED).

**Actor ngoài hệ thống:**
- **Đối tác vận chuyển (External Shipping System)**: Trong thực tế là GIAO HÀNG NHANH / VNPOST. Trong assignment, Staff sẽ đóng vai trò cập nhật thủ công trạng thái vận chuyển.

---

## 2. Actors & Use Cases

### Actors:
- **Customer** — Theo dõi trạng thái giao hàng
- **Staff** — Cập nhật trạng thái, gán tài xế
- **Admin** — Xem tổng quan vận chuyển
- **Order Service** — Gửi event `order.created` để kích hoạt Shipment
- **Payment Service** — Gửi event khi COD thu tiền thành công

### Use Case Tổng Quan:
```
[Shipping Context]
    │
    ├── UC01: Xem trạng thái & lịch sử giao hàng ─── Customer
    ├── UC02: Tạo Shipment khi đặt hàng ────────── Order Service (consume event)
    ├── UC03: Gán tài xế cho đơn ──────────────── Staff
    ├── UC04: Cập nhật trạng thái vận chuyển ────── Staff
    ├── UC05: Xác nhận kết quả giao hàng ───────── Staff
    ├── UC06: Xem danh sách Shipment ──────────── Staff, Admin
    └── UC07: Quản lý Courier ────────────────── Admin
```

| UC | Tên | Actor | Mô tả ngắn |
|---|---|---|---|
| UC01 | Xem trạng thái | Customer | Xem Shipment.status + danh sách checkpoint lịch sử của đơn hàng (status history, không cần live map) |
| UC02 | Tạo Shipment | Order Service | Consume `order.created` → tạo Shipment (AWAITING_PAYMENT hoặc PROCESSING) |
| UC03 | Gán tài xế | Staff | Assign Courier cho Shipment |
| UC04 | Cập nhật status | Staff | Chuyển trạng thái: PROCESSING → SHIPPING; thêm checkpoint văn bản |
| UC05 | Kết quả giao hàng | Staff | **Luồng chính:** DELIVERED → publish event + trigger COD payment. **Luồng thay thế:** FAILED → ghi lý do, chờ xử lý lại |
| UC06 | Xem danh sách | Staff/Admin | Lọc theo status, ngày |
| UC07 | Quản lý Courier | Admin | CRUD Courier, xem trạng thái sẵn sàng |

---

## 3. Entities & Attributes

### 3.1 `Shipment` — Aggregate Root
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| order_id | int | Soft ref → Order (KHÔNG dùng FK vật lý) |
| customer_id | int | Soft ref → Customer |
| address | text | **Snapshot** địa chỉ lúc đặt hàng |
| courier_id | int (nullable) | FK nội bộ → Courier |
| method | string | standard / fast / express |
| fee | float | Phí vận chuyển |
| tracking_number | string (nullable) | |
| status | string | AWAITING_PAYMENT / PROCESSING / SHIPPING / DELIVERED / FAILED |
| created_at | datetime | |
| shipped_at | datetime (nullable) | Thời điểm xuất kho |
| delivered_at | datetime (nullable) | Thời điểm giao thành công |
| note | text (nullable) | Ghi chú giao hàng |

### 3.2 `Courier` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| name | string | |
| phone | string | |
| email | string (nullable) | |
| current_location | string (nullable) | Địa chỉ/tọa độ hiện tại |
| is_available | boolean | Có thể nhận thêm đơn không |
| vehicle_type | string | bike / motorbike / truck |

### 3.3 `ShippingTracking` — Entity (thuộc Shipment Aggregate)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| shipment_id | int (FK → Shipment) | |
| checkpoint | string | "Rời kho trung chuyển", "Đang giao", ... |
| location | string (nullable) | Vị trí vật lý |
| status_code | string | Mã trạng thái tại checkpoint |
| timestamp | datetime | |

---

## 4. Relationships

| Quan hệ | Từ | Đến | Loại | Cardinality |
|---|---|---|---|---|
| Composition | Shipment | ShippingTracking | has-parts (cascade delete) | 1..1 → 0..* |
| Association | Courier | Shipment | manages | 0..1 → 0..* |
| Association (Logical) | Shipment | Order (Order Context) | by ID | 0..* → 1..1 |
| Association (Logical) | Shipment | Customer (User Context) | by ID | 0..* → 1..1 |

---

## 5. Luồng Hoạt Động Cơ Bản

### Flow UC03: Tạo Shipment (consume RabbitMQ)
```
[RabbitMQ] order.created event received
  Parse: order_id, customer_id, shipping_address, payment_method

  Nếu payment_method = 'online':
    Tạo Shipment(status=AWAITING_PAYMENT)
    Chờ event payment.completed → chuyển status=PROCESSING

  Nếu payment_method = 'cod':
    Tạo Shipment(status=PROCESSING) ngay
    Tạo ShippingTracking(checkpoint="Đơn hàng được xác nhận")
```

### Flow UC05 + UC06: Cập nhật và Hoàn tất Giao Hàng
```
Staff → PATCH /shipments/{id}/status
  Body: { status: "SHIPPING", checkpoint: "Đang trên đường giao" }

  1. Cập nhật Shipment.status
  2. Tạo ShippingTracking record
  3. Cập nhật Shipment.shipped_at (nếu status = SHIPPING)

Staff → POST /shipments/{id}/delivered
  1. Shipment.status = DELIVERED
  2. Shipment.delivered_at = now()
  3. Tạo ShippingTracking(checkpoint="Đã giao thành công")
  4. Publish event "shipment.status_changed" {status: DELIVERED}
     → Order Service consume → Order.status = COMPLETED
     (Nếu COD): → Payment Service consume → Payment.status = COD_PAID
```

### Flow UC07: Xử lý giao thất bại
```
Staff → POST /shipments/{id}/failed
  Body: { reason: "Khách không có mặt" }
  1. Shipment.status = FAILED
  2. Tạo ShippingTracking(checkpoint="Giao thất bại: " + reason)
  3. Publish event "shipment.failed" → Order Service
     (Order có thể xử lý re-delivery hoặc cancel)
```

---

## 6. API Endpoints Chính

| Method | Endpoint | Actor | Mô tả |
|---|---|---|---|
| GET | `/shipments/{order_id}` | Customer | Trạng thái giao hàng đơn của mình |
| GET | `/shipments/{order_id}/tracking` | Customer | Lộ trình chi tiết |
| GET | `/shipments/` | Staff/Admin | Danh sách shipment |
| PATCH | `/shipments/{id}/assign-courier` | Staff | Gán tài xế |
| PATCH | `/shipments/{id}/status` | Staff | Cập nhật trạng thái |
| POST | `/shipments/{id}/delivered` | Staff | Xác nhận giao thành công |
| POST | `/shipments/{id}/failed` | Staff | Giao thất bại |
| GET | `/couriers/` | Admin | Danh sách tài xế |
| POST | `/couriers/` | Admin | Thêm tài xế |
| PATCH | `/couriers/{id}` | Admin | Cập nhật tài xế |

---

## 7. RabbitMQ Events

| Event | Subscribe | Publish |
|---|---|---|
| `order.created` | ✅ (tạo Shipment) | — |
| `payment.completed` | ✅ (activate Shipment từ AWAITING → PROCESSING) | — |
| `shipment.status_changed` | — | ✅ (khi status thay đổi) |
| `shipment.failed` | — | ✅ (khi giao thất bại) |

---

## 8. Django Apps Nội Bộ

```
shipping_service/
├── shipments/    ← Shipment, ShippingTracking + views + event consumer
└── couriers/     ← Courier management
```

## 9. Ghi Chú Migration

- Source: `order_service/shipping/` app
- Thêm: `Courier`, `ShippingTracking` (models mới)
- Đổi tên: `Shipping` → `Shipment`
- Tạo database mới: `shipping_db`
