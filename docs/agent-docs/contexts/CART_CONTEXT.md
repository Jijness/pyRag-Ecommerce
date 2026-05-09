# Cart Context — Thiết Kế Chi Tiết

**Service:** `cart_service` | **Port:** 8003 | **Database:** `cart_db`

---

## 1. Mô Tả Bounded Context

Cart Context hoạt động như một **vùng đệm lưu trữ tạm thời** trước khi khách hàng chốt đơn. Đặc thù của context này là tần suất I/O cực cao nhưng dữ liệu có vòng đời ngắn (xóa khi checkout thành công hoặc hết hạn session).

Context này tách biệt hoàn toàn khỏi Order — Cart chỉ lưu **ý định mua hàng**, còn Order mới là giao dịch thực sự.

---

## 2. Actors & Use Cases

### Actors:
- **Customer** — Khách hàng đã đăng nhập
- **Guest** — Khách vãng lai (cart gắn với session_id)
- **Order Service** — Gọi API lấy cart items khi checkout

### Use Case Tổng Quan:
```
[Cart Context]
    │
    ├── UC01: Xem giỏ hàng ─────────────────── Customer, Guest
    ├── UC02: Thêm sản phẩm vào giỏ ────────── Customer, Guest
    ├── UC03: Cập nhật số lượng item ────────── Customer, Guest
    ├── UC04: Xóa item khỏi giỏ ────────────── Customer, Guest
    ├── UC05: Xóa toàn bộ giỏ hàng ─────────── Customer
    ├── UC06: Xem tóm tắt giỏ (tổng tiền) ──── Customer, Guest
    └── UC07: Deactivate giỏ (sau checkout) ─── Order Service
```

| UC | Tên | Actor | Mô tả ngắn |
|---|---|---|---|
| UC01 | Xem giỏ | Customer/Guest | Trả về danh sách items + tổng tiền (giá call từ Product Service) |
| UC02 | Thêm vào giỏ | Customer/Guest | Thêm product_id + quantity; nếu đã có thì cộng dồn quantity |
| UC03 | Cập nhật SL | Customer/Guest | PATCH quantity của CartItem |
| UC04 | Xóa item | Customer/Guest | Xóa CartItem theo item_id |
| UC05 | Xóa giỏ | Customer | Xóa toàn bộ CartItems của giỏ (clear cart) |
| UC06 | Tóm tắt | Customer/Guest | Tính tổng tiền bằng cách gọi Product Service lấy giá real-time |
| UC07 | Deactivate | Order Service | Đặt Cart.is_active = False sau khi checkout thành công |

---

## 3. Entities & Attributes

### 3.1 `Cart` — Aggregate Root
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_id | int | Soft ref → User; null nếu Guest |
| session_id | string | Dành cho Guest (hash từ cookie) |
| is_active | boolean | False = đã checkout |
| created_at | datetime | |
| updated_at | datetime | Dùng cho batch job dọn cart cũ |

### 3.2 `CartItem` — Entity (thuộc Cart Aggregate)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| cart_id | int (FK → Cart) | |
| product_id | int | Soft ref → Product (KHÔNG lưu price tại đây) |
| quantity | int | > 0 |
| added_at | datetime | |

> **Lưu ý kỹ thuật:** `CartItem` KHÔNG lưu `price`. Giá được lấy real-time từ Product Service khi hiển thị tóm tắt giỏ. Điều này đảm bảo giá luôn cập nhật khi Product Service thay đổi giá.

---

## 4. Relationships

| Quan hệ | Từ | Đến | Loại | Cardinality |
|---|---|---|---|---|
| Composition | Cart | CartItem | has-parts (cascade delete) | 1..1 → 0..* |
| Association (Logical) | CartItem | Product (Product Context) | references by ID | 0..* → 1..1 |
| Association (Logical) | Cart | User (User Context) | references by ID | 0..* → 0..1 |

---

## 5. Luồng Hoạt Động Cơ Bản

### Flow UC02: Thêm sản phẩm vào giỏ
```
Customer → POST /cart/items
  Body: { product_id: 5, quantity: 2 }

  1. Lấy/tạo Cart active của customer_id
  2. Kiểm tra CartItem có product_id=5 chưa?
     - Có: tăng quantity += 2
     - Chưa: tạo CartItem mới
  3. Cập nhật Cart.updated_at
  4. Trả về Cart summary
```

### Flow UC06: Xem tóm tắt giỏ (API Composition)
```
Customer → GET /cart/summary

  1. Lấy Cart + CartItems của customer
  2. Collect [product_id, quantity] từ CartItems
  3. Gọi Product Service: GET /products/?ids=1,2,3 (batch fetch giá)
  4. Tính: subtotal = Σ (quantity × price)
  5. Trả về:
     {
       cart_id, items: [{product_id, name, price, quantity, subtotal}],
       total_items, subtotal_total
     }
```

### Flow UC07: Deactivate (gọi từ Order Service)
```
Order Service → PATCH /cart/{cart_id}/deactivate
  1. Verify internal service token
  2. Đặt Cart.is_active = False
  3. Không xóa CartItems (giữ lại lịch sử)
```

---

## 6. API Endpoints Chính

| Method | Endpoint | Actor | Mô tả |
|---|---|---|---|
| GET | `/cart/` | Customer/Guest | Xem giỏ hàng hiện tại |
| POST | `/cart/items` | Customer/Guest | Thêm item vào giỏ |
| PATCH | `/cart/items/{item_id}` | Customer/Guest | Cập nhật quantity |
| DELETE | `/cart/items/{item_id}` | Customer/Guest | Xóa item |
| DELETE | `/cart/clear` | Customer | Xóa toàn bộ giỏ |
| GET | `/cart/summary` | Customer/Guest | Tóm tắt + tổng tiền |
| PATCH | `/cart/{cart_id}/deactivate` | Order Service (internal) | Đánh dấu đã checkout |

---

## 7. Django Apps Nội Bộ

```
cart_service/
└── cart/     ← Cart, CartItem models + views
```

## 8. Ghi Chú Migration

- Source: `order_service/cart/` app
- Đổi `CartItem.book_id` → `CartItem.product_id`
- Tạo database mới: `cart_db`
- Cập nhật `api_gateway` routing: `/cart/` → `cart_service:8003`
