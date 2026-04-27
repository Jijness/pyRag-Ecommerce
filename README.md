# ShopX Marketplace

**ShopX** là hệ thống thương mại điện tử được thiết kế theo mô hình **Domain-Driven Design (DDD)** và **Microservices Architecture**, kết hợp với **AI Recommendation Engine** dựa trên Knowledge Graph (Neo4j) và hành vi người dùng.

> Đây là bài tập lớn môn **Kiến trúc và Thiết kế Phần mềm (SoAD)** – GVHD: Trần Đình Quế

---

## Kiến trúc tổng quan

```
Frontend (4000) → API Gateway (8000) → [Microservices]
                                             ↓
                                    MySQL (per-service DB)
                                    Neo4j (RAG Knowledge Graph)
                                    RabbitMQ (Async events)
```

### Tech Stack

| Layer              | Technology                          |
|--------------------|-------------------------------------|
| **Core Services**  | Django 5.x + Django REST Framework  |
| **AI Services**    | FastAPI + Neo4j + LSTM              |
| **Database**       | MySQL 8.0 (per-service)             |
| **Knowledge Graph**| Neo4j 5.x                           |
| **Message Broker** | RabbitMQ 3                          |
| **Container**      | Docker + Docker Compose             |
| **Frontend**       | Vanilla JS SPA                      |

---

## Danh sách Services

| Service              | Port  | Framework     | Bounded Context          |
|----------------------|-------|---------------|--------------------------|
| `api_gateway`        | 8000  | Nginx/Python  | Gateway                  |
| `auth_service`       | 8001  | Django + DRF  | Identity & Access        |
| `product_service`    | 8002  | Django + DRF  | Catalog                  |
| `order_service`      | 8003  | Django + DRF  | Order & Checkout (Cart, Payment, Shipping) |
| `customer_service`   | 8004  | FastAPI       | Customer Profile         |
| `staff_service`      | 8005  | FastAPI       | Staff & Admin            |
| `marketing_service`  | 8006  | FastAPI       | Promotions & Marketing   |
| `inventory_service`  | 8007  | FastAPI       | Inventory & Procurement  |
| `content_service`    | 8008  | FastAPI       | Content & CMS            |
| `interaction_service`| 8009  | FastAPI       | Loyalty & Gift Cards     |
| `analytics_service`  | 8010  | FastAPI       | Analytics & Reports      |
| `notification_service`| 8011 | FastAPI      | Notifications            |
| `ai_chat_service`    | 8012  | FastAPI       | AI RAG Recommendation    |
| `behavior_service`   | 8013  | FastAPI       | User Behavior Tracking   |

### Infrastructure

| Service    | Port (host) | Mô tả                        |
|------------|-------------|-------------------------------|
| MySQL      | 3307        | Database cho tất cả service  |
| Neo4j      | 7474 / 7687 | Knowledge Graph RAG           |
| RabbitMQ   | 5672 / 15672| Message broker / Management  |

---

## Luồng nghiệp vụ chính

### Checkout Flow
```
Customer bấm "Đặt hàng" 
  → POST /orders/checkout 
  → Order (PENDING) + Payment (Pending) + Shipping (PENDING) được tạo 
  → Giỏ hàng deactivate
```

### RAG Auto-sync (Sản phẩm mới)
```
Staff tạo/sửa sản phẩm (product_service) 
  → trigger_ai_sync() 
  → POST http://ai_chat_service:8012/sync-product 
  → upsert_product() cập nhật Node trong Neo4j ngay lập tức
```

### User Behavior → Recommendation
```
User tương tác (view/cart/search) 
  → behavior_service ghi nhận event 
  → graph_sync.py cập nhật đồ thị Neo4j 
  → ai_chat_service truy vấn graph để cá nhân hóa gợi ý
```

---

## Cách chạy

### Yêu cầu
- Docker Desktop đang chạy
- Docker Compose v2+

### Khởi động toàn bộ hệ thống

```bash
docker compose up -d --build
```

### Sau lần đầu build, chạy migrate cho order_service

```bash
docker compose exec order_service python manage.py migrate --fake-initial
```

### Seed dữ liệu demo

```bash
python seed_data.py
```

### Dừng hệ thống

```bash
docker compose down
```

---

## URLs quan trọng

| Trang               | URL                              |
|---------------------|----------------------------------|
| Frontend            | http://localhost:4000            |
| API Gateway         | http://localhost:8000            |
| Neo4j Browser       | http://localhost:7474            |
| RabbitMQ Management | http://localhost:15672           |
| AI Chat API docs    | http://localhost:8012/docs       |

---

## Tài khoản Demo

| Loại     | Email / Username     | Password   |
|----------|----------------------|------------|
| Customer | demo@shopx.vn        | demo123    |
| Staff    | admin                | admin123   |

---

## Cấu trúc thư mục

```
assignment_6_ddd_marketplace/
├── backend-services/
│   ├── auth_service/          # Django + DRF
│   ├── product_service/       # Django + DRF + RAG Webhook
│   ├── order_service/         # Django + DRF (cart, orders, payment, shipping)
│   ├── customer_service/      # FastAPI
│   ├── marketing_service/     # FastAPI
│   ├── inventory_service/     # FastAPI
│   ├── ai_chat_service/       # FastAPI + Neo4j RAG
│   ├── behavior_service/      # FastAPI + Neo4j Graph Sync
│   └── ...
├── frontend/                  # Vanilla JS SPA
├── docs/
│   ├── agent-docs/            # Tài liệu kiến trúc cho AI Agent
│   └── raw-docs/              # Đề bài & form tiểu luận
├── mysql-init/                # Script khởi tạo databases
├── docker-compose.yml
└── README.md
```

---

## Tài liệu bổ sung

- [Kiến trúc chi tiết](docs/agent-docs/ARCHITECTURE.md)
- [Hướng dẫn AI Service](docs/agent-docs/AI_SERVICE_ASSIGNMENT_REPORT.md)
- [Sequence Diagrams](docs/agent-docs/SEQUENCE_DIAGRAMS_VP.md)
- [DDD Refactor Notes](docs/agent-docs/DDD_REFACTOR_NOTES.md)
