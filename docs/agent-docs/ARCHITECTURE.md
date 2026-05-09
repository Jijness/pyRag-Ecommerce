# Kiến Trúc Tổng Thể — PyRag E-Commerce Microservices

## 1. Tổng Quan

**PyRag E-Commerce** là hệ thống thương mại điện tử được xây dựng theo **Domain-Driven Design (DDD)** và **Microservices Architecture**. Toàn bộ hệ thống được triển khai bằng **Django + Django REST Framework (DRF)**, containerized bằng Docker Compose.

### Nguyên tắc kiến trúc cốt lõi:
- **Database per Service** — Mỗi Bounded Context sở hữu một database MySQL riêng biệt
- **Soft Reference by ID** — Không có khóa ngoại vật lý xuyên service
- **API Contract** — Giao tiếp đồng bộ qua REST API
- **Event-Driven (RabbitMQ)** — Giao tiếp bất đồng bộ cho các luồng Saga và notification
- **Security: JWT + Bcrypt** — Xác thực phi trạng thái, mật khẩu mã hóa Bcrypt

---

## 2. Sơ Đồ Kiến Trúc Tổng Thể

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client / Frontend (4000)                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/REST
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  API Gateway — Django (8000)                    │
│   JWT Verification · RBAC Check · Request Routing · Nginx(4000) │
└──┬──────┬──────┬──────┬──────┬──────┬────────────┬──────────────┘
   │      │      │      │      │      │            │
   ▼      ▼      ▼      ▼      ▼      ▼            ▼
 user  product  cart  order  payment shipping      ai
(8001) (8002)  (8003)(8004) (8005)   (8006)      (8007)
   │      │      │      │      │      │            │
   └──────┴──────┴──────┴──────┴──────┴────────────┘
                  RabbitMQ (5672)
                  (Async Events)

Infrastructure:
  MySQL (3307) · Neo4j (7474/7687) · RabbitMQ (5672/15672)
```

---

## 3. Danh Sách Services

| Service | Port | Database | Framework | Bounded Context |
|---|---|---|---|---|
| `api_gateway` | 8000 | — | **Django** | Gateway & Auth Middleware |
| `user_service` | 8001 | `user_db` | Django | User Context |
| `product_service` | 8002 | `product_db` | Django | Product Context |
| `cart_service` | 8003 | `cart_db` | Django | Cart Context |
| `order_service` | 8004 | `order_db` | Django | Order Context |
| `payment_service` | 8005 | `payment_db` | Django | Payment Context |
| `shipping_service` | 8006 | `shipping_db` | Django | Shipping Context |
| `ai_service` | 8007 | `ai_db` + Neo4j | Django | AI & Recommendation Context |

---

## 4. Actors Hệ Thống

| Actor | Mô tả | Quyền truy cập |
|---|---|---|
| **Guest** | Khách vãng lai chưa đăng nhập | Duyệt sản phẩm, tìm kiếm, xem giỏ (session) |
| **Customer** | Khách hàng đã đăng nhập | Tất cả quyền Guest + Đặt hàng, Thanh toán, Chat AI |
| **Staff** | Nhân viên | Quản lý sản phẩm, duyệt nhập kho, cập nhật vận chuyển, xem đơn hàng |
| **Admin** | Quản trị viên | Toàn quyền + Quản lý Staff, Phân quyền, Báo cáo |
| **Payment System** | Cổng thanh toán (giả lập) | Gọi webhook callback khi thanh toán xong/thất bại |
| **Shipping System** | Đối tác vận chuyển (giả lập) | Cập nhật trạng thái lộ trình |

---

## 5. Giao Tiếp Giữa Các Service

### 5.1 Synchronous — REST API
- **api_gateway** → mọi service (proxy + JWT verify)
- **order_service** → product_service (kiểm tra stock khi checkout)
- **order_service** → cart_service (lấy cart items và snapshot giá tại thời điểm đó khi checkout)
- **ai_service** → product_service (lấy thông tin sản phẩm cho RAG)
- **ai_service** → user_service (lấy customer profile cho personalization)

### 5.2 Asynchronous — RabbitMQ Events

| Event | Publisher | Subscriber(s) |
|---|---|---|
| `order.created` | order_service | payment_service, shipping_service |
| `payment.completed` | payment_service | order_service (cập nhật status) |
| `payment.failed` | payment_service | order_service (Saga compensation) |
| `shipment.status_changed` | shipping_service | order_service |
| `product.synced` | product_service | ai_service (cập nhật Neo4j) |
| `behavior.event` | (Frontend/Gateway) | ai_service (log hành vi) |

---

## 6. Infrastructure

| Component | Port | Mục đích |
|---|---|---|
| MySQL 8.0 | 3307 (host) / 3306 (internal) | RDBMS cho tất cả Django services |
| Neo4j 5.x | 7474 (Browser), 7687 (Bolt) | Knowledge Graph cho AI RAG |
| RabbitMQ 3 | 5672 (AMQP), 15672 (Management) | Message Broker cho async events |

---

## 7. Bảo Mật

- **JWT (JSON Web Token)**: API Gateway verify token trước khi forward request
- **Bcrypt**: Mã hóa password tại `user_service`
- **RBAC**: Role-based access (guest/customer/staff/admin) kiểm tra tại từng service
- **Soft Reference**: Không có cross-database FK, ngăn data leak qua JOIN

---

## 8. Ghi Chú Migration

> Một số field trong database hiện tại vẫn dùng tên cũ `book_id` (legacy từ phiên bản BookStore).
> Khi tạo service mới, các field này sẽ được chuẩn hóa thành `product_id`.
> Service cũ đang chạy KHÔNG bị sửa cho đến khi migration được thực hiện theo từng pha.
