# Product Context — Thiết Kế Chi Tiết

**Service:** `product_service` | **Port:** 8002 | **Database:** `product_db`

---

## 1. Mô Tả Bounded Context

Product Context bọc gói toàn bộ **vòng đời của sản phẩm**: từ thông tin danh mục, quản lý tồn kho và nhập hàng, đến nội dung CMS hiển thị trên frontend và khuyến mãi gắn với catalog. Đây là context tự trị nhất — không phụ thuộc vào bất kỳ context nào khác khi phục vụ luồng đọc (duyệt sản phẩm, tìm kiếm).

**Nguyên tắc DDD quan trọng:** Ranh giới thiết kế dựa trên **hành vi hệ thống**, không tách service theo loại sản phẩm vật lý. Mọi sản phẩm đều đi qua cùng một `Product` Aggregate Root; sự khác biệt về thuộc tính đặc thù được xử lý qua **Multi-table Inheritance**.

---

## 2. Actors & Use Cases

### Actors:
- **Guest** — Người dùng chưa đăng nhập
- **Customer** — Khách hàng đã đăng nhập
- **Staff** — Nhân viên (quản lý sản phẩm, kho)
- **Admin** — Quản trị viên
- **AI Service** — Service AI gọi sang để sync dữ liệu

### Use Case Tổng Quan:

```
[Product Context]
    │
    ├── UC01: Duyệt danh mục sản phẩm ─────── Guest, Customer
    ├── UC02: Xem chi tiết sản phẩm ────────── Guest, Customer
    ├── UC03: Tìm kiếm sản phẩm ────────────── Guest, Customer
    ├── UC04: Xem đánh giá sản phẩm ────────── Guest, Customer
    ├── UC05: Viết đánh giá / xếp hạng ─────── Customer
    ├── UC06: Thêm sản phẩm mới ────────────── Staff, Admin
    ├── UC07: Cập nhật thông tin sản phẩm ──── Staff, Admin
    ├── UC08: Xóa / ẩn sản phẩm ────────────── Admin
    ├── UC09: Quản lý danh mục ─────────────── Admin
    ├── UC10: Nhập hàng từ nhà cung cấp ────── Staff
    ├── UC11: Xem tồn kho ───────────────────── Staff, Admin
    ├── UC12: Điều chỉnh tồn kho thủ công ──── Staff
    ├── UC13: Xem cảnh báo tồn kho thấp ────── Staff, Admin
    ├── UC14: Quản lý khuyến mãi / Flash Sale ── Admin
    ├── UC15: Quản lý Banner / Collection ──── Admin
    └── UC16: Sync sản phẩm sang AI (Webhook)── AI Service
```

| UC | Tên | Actor | Mô tả ngắn |
|---|---|---|---|
| UC01 | Duyệt catalog | Guest/Customer | Lọc theo danh mục, sắp xếp giá/mới nhất |
| UC02 | Xem chi tiết | Guest/Customer | Xem thông tin đầy đủ + variants + reviews |
| UC03 | Tìm kiếm | Guest/Customer | Tìm theo keyword, trả về danh sách sản phẩm |
| UC04 | Xem review | Guest/Customer | Xem danh sách đánh giá của sản phẩm |
| UC05 | Viết review | Customer | Thêm đánh giá (sau khi đã mua hàng) |
| UC06 | Thêm SP | Staff/Admin | Tạo product + chọn loại (Book/Electronics/...) |
| UC07 | Sửa SP | Staff/Admin | Cập nhật giá, mô tả, tồn kho, ảnh |
| UC08 | Xóa SP | Admin | Soft-delete (ẩn khỏi catalog) |
| UC09 | Quản lý DM | Admin | CRUD Category (tree structure) |
| UC10 | Nhập hàng | Staff | Tạo PurchaseOrder từ Supplier, nhập kho |
| UC11 | Xem kho | Staff/Admin | Xem stock hiện tại, lịch sử nhập/xuất |
| UC12 | Điều chỉnh kho | Staff | Tạo InventoryLog: IN/OUT/ADJUSTMENT |
| UC13 | Cảnh báo kho | Staff/Admin | Xem danh sách sản phẩm dưới ngưỡng threshold |
| UC14 | Khuyến mãi | Admin | Tạo/sửa Promotion, FlashSale, Bundle |
| UC15 | CMS | Admin | Tạo/sửa Banner, Collection, BlogPost |
| UC16 | Webhook sync | AI Service | Nhận POST khi product được tạo/cập nhật → sync Neo4j |

---

## 3. Entities & Attributes

### 3.1 `Category` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| name | string | |
| slug | string (unique) | URL-friendly |
| description | text | |
| parent_id | int (self-FK) | Cây phân cấp danh mục |
| image_url | string | |
| is_active | boolean | |

### 3.2 `Product` — Aggregate Root
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| name | string | |
| sku | string (unique) | Mã kho hàng |
| base_price | decimal | Giá gốc |
| stock | int | Tồn kho hiện tại |
| category_id | int (FK → Category) | |
| description | text | |
| image_url | string | |
| attributes | JSONField | Thuộc tính linh hoạt (thông số kỹ thuật) |
| is_active | boolean | Ẩn/hiện khỏi catalog |
| created_at | datetime | |

### 3.3 Product Type Inheritance (Multi-table Inheritance)

**`Book`** ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| author | string |
| isbn | string |
| publisher | string |
| genre | string |
| language | string |
| pages | int |

**`Electronics`** ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| brand | string |
| model_number | string |
| warranty_months | int |
| voltage | string |

**`Fashion`** ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| material | string |
| gender | string (male/female/unisex) |
| size_chart | JSONField |

**`Toy`** ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| age_range | string |
| safety_cert | string |
| material | string |

**`Stationery`** (Dụng cụ học tập) ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| type | string |
| brand | string |
| color | string |

**`DrinkwareContainer`** (Bình nước) ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| capacity_ml | int |
| material | string |
| insulated | boolean |

**`DeskDecor`** (Đồ trang trí bàn học) ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| dimensions | string |
| material | string |
| theme | string |

**`GiftSet`** (Gói quà) ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| occasion | string |
| includes_description | text |
| packaging_type | string |

**`Backpack`** (Ba lô) ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| capacity_liters | float |
| dimensions | string |
| material | string |
| compartments | int |

**`ArtSupply`** (Mỹ thuật) ← kế thừa `Product`
| Thuộc tính | Kiểu |
|---|---|
| medium | string |
| brand | string |
| piece_count | int |

### 3.4 `ProductVariant` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| product_id | int (FK → Product) | |
| sku | string (unique) | SKU riêng cho variant |
| color | string | |
| size | string | |
| additional_price | decimal | Giá cộng thêm so với base_price |
| stock | int | Tồn kho cho variant này |

### 3.5 `Rating` — Entity
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| product_id | int (FK → Product) |
| customer_id | int | Soft ref → User |
| score | float (1-5) |
| created_at | datetime |

### 3.6 `Review` — Entity
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| product_id | int (FK → Product) |
| customer_id | int | Soft ref → User |
| body | text |
| created_at | datetime |

### 3.7 Inventory Entities

**`Supplier`**
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| name | string |
| contact_name | string |
| email | string |
| phone | string |
| address | text |
| is_active | boolean |

**`Warehouse`**
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| name | string |
| location | string |
| capacity | int |

**`PurchaseOrder`**
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| supplier_id | int (FK → Supplier) |
| total_amount | float |
| status | string (DRAFT/ORDERED/RECEIVED) |
| order_date | datetime |
| received_date | datetime |

**`PurchaseOrderItem`**
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| purchase_order_id | int (FK) |
| product_id | int (FK → Product) |
| quantity | int |
| unit_cost | float |

**`InventoryLog`**
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| warehouse_id | int (FK → Warehouse) |
| product_id | int (FK → Product) |
| change_type | string (IN/OUT/ADJUSTMENT) |
| quantity | int |
| note | string |
| timestamp | datetime |

**`InventoryAlert`**
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| product_id | int (FK → Product) |
| threshold | int |
| current_stock | int |
| is_resolved | boolean |

### 3.8 Promotion Entities

**`Promotion`** | `FlashSale`
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| name | string |
| discount_percent | float |
| product_id / category_id | int (FK → Product/Category) |
| start_date / end_date | datetime |
| is_active | boolean |
| max_quantity (FlashSale) | int |

**`Bundle`**
| Thuộc tính | Kiểu |
|---|---|
| id | int |
| name | string |
| price | float |
| product_ids | JSONField |

### 3.9 Content Entities

**`Banner`** | `Collection`  | `BlogPost`
(Xem `content_service` models — giữ nguyên structure, chỉ di chuyển vào `product_service/content/`)

---

## 4. Relationships

| Quan hệ | Từ | Đến | Loại | Cardinality |
|---|---|---|---|---|
| Association | Product | Category | belongs-to | 0..* → 1..1 |
| Inheritance | Book/Electronics/..(10 types) | Product | is-a | — |
| Composition | Product | ProductVariant | has-parts (cascade delete) | 1..1 → 0..* |
| Composition | Product | Rating | has-parts (cascade delete) | 1..1 → 0..* |
| Composition | Product | Review | has-parts (cascade delete) | 1..1 → 0..* |
| Composition | PurchaseOrder | PurchaseOrderItem | has-parts | 1..1 → 1..* |
| Association | PurchaseOrder | Supplier | belongs-to | 0..* → 1..1 |
| Association | InventoryLog | Warehouse | references | 0..* → 0..1 |
| Association | InventoryLog | Product | references | 0..* → 1..1 |
| Association | Promotion/FlashSale | Product | references | 0..* → 0..1 |

**Quan hệ Xuyên Domain (Soft Reference):**
- `Rating.customer_id` → User.id
- `Review.customer_id` → User.id
- `CartItem.product_id` → Product.id
- `OrderItem.product_id` → Product.id

---

## 5. Luồng Hoạt Động Cơ Bản

### Flow UC03: Tìm Kiếm
```
Guest/Customer → GET /products/search?q=laptop&category=2&sort=price
  1. Query Product table (LIKE + filter)
  2. Join Category nội bộ
  3. Lọc is_active=True
  4. Sort, paginate
  5. Trả về list [{ id, name, base_price, image_url, category, stock }]
```

### Flow UC06 + UC16: Thêm Sản Phẩm → Sync AI
```
Staff → POST /products/
  1. Tạo Product (base table)
  2. Tạo record loại kế thừa tương ứng (Book/Electronics/...)
  3. Update Product.stock
  4. Sau khi lưu thành công:
     → publish event "product.synced" → RabbitMQ
     → AI Service consume event → cập nhật Neo4j Knowledge Graph
```

### Flow UC10: Nhập Hàng
```
Staff → POST /inventory/purchase-orders
  1. Tạo PurchaseOrder (status=DRAFT)
  2. Thêm PurchaseOrderItem
  3. POST /inventory/purchase-orders/{id}/receive
     → Cập nhật status=RECEIVED
     → Tạo InventoryLog (type=IN) cho từng item
     → Cập nhật Product.stock
     → Kiểm tra InventoryAlert: nếu stock > threshold → is_resolved=True
```

---

## 6. API Endpoints Chính

| Method | Endpoint | Actor | Mô tả |
|---|---|---|---|
| GET | `/products/` | Guest/Customer | Duyệt catalog (filter, sort, paginate) |
| GET | `/products/{id}` | Guest/Customer | Chi tiết sản phẩm |
| GET | `/products/search` | Guest/Customer | Tìm kiếm theo keyword |
| POST | `/products/` | Staff/Admin | Tạo sản phẩm mới |
| PATCH | `/products/{id}` | Staff/Admin | Cập nhật |
| DELETE | `/products/{id}` | Admin | Soft delete |
| GET | `/products/{id}/reviews` | Guest | Xem reviews |
| POST | `/products/{id}/reviews` | Customer | Gửi review |
| GET | `/categories/` | Guest | Danh sách danh mục |
| POST | `/inventory/purchase-orders` | Staff | Tạo đơn nhập hàng |
| POST | `/inventory/purchase-orders/{id}/receive` | Staff | Nhận hàng → update stock |
| GET | `/inventory/alerts` | Staff/Admin | Cảnh báo tồn kho thấp |
| GET | `/promotions/` | Guest | Xem khuyến mãi đang chạy |
| POST | `/promotions/flash-sales` | Admin | Tạo Flash Sale |

---

## 7. Django Apps Nội Bộ

```
product_service/
├── catalog/        ← Category, Product + 10 inheritance types, Variant, Rating, Review
├── inventory/      ← Supplier, Warehouse, PurchaseOrder, InventoryLog, InventoryAlert
├── promotions/     ← Promotion, FlashSale, Discount, Bundle
└── content/        ← Banner, Collection, BlogPost
```
