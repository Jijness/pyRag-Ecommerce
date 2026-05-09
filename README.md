# ShopX Marketplace - DDD Microservices Architecture

**ShopX** là hệ thống thương mại điện tử được thiết kế theo mô hình **Domain-Driven Design (DDD)** và **Microservices Architecture**, kết hợp với **AI Recommendation Engine** dựa trên Knowledge Graph (Neo4j) và Deep Learning Behavior Models.

> Dự án này đã được chuyển đổi hoàn toàn sang kiến trúc Microservices thuần Django (DDD compliant).

---

## Kiến trúc tổng quan

```
Frontend (4000) → API Gateway (8000 - Django) → [Microservices]
                                                     ↓
                                            MySQL (per-service DB)
                                            Neo4j (Knowledge Graph RAG)
                                            RabbitMQ (Saga Orchestration)
```

### Tech Stack

| Layer              | Technology                          |
|--------------------|-------------------------------------|
| **API Gateway**    | Django (Reverse Proxy + Auth)       |
| **Core Services**  | Django 4.2+ / FastAPI (Unified Stack)|
| **AI Services**    | Django + DL Models + Neo4j          |
| **Database**       | MySQL 8.0 (7 isolated DBs)          |
| **Knowledge Graph**| Neo4j 5.x                           |
| **Message Broker** | RabbitMQ 3                          |
| **Container**      | Docker + Resource Limits            |

---

## Danh sách Services (7 DDD Contexts)

| Service              | Port  | Framework     | Bounded Context             |
|----------------------|-------|---------------|-----------------------------|
| `api_gateway`        | 8000  | Django        | Central Entry Point         |
| `user_service`       | 8001  | Django + DRF  | Identity & Access (Auth)    |
| `product_service`    | 8002  | Django + DRF  | Catalog & Inventory         |
| `cart_service`       | 8003  | Django + DRF  | Shopping Cart               |
| `order_service`      | 8004  | Django + DRF  | Order Orchestration         |
| `payment_service`    | 8005  | Django + DRF  | Payment Processing          |
| `shipping_service`   | 8006  | Django + DRF  | Logistics & Shipping        |
| `ai_service`         | 8007  | Django + ML   | RAG & Behavioral AI         |

---

## Tính năng AI nổi bật

1. **Behavioral AI**: Phân loại người dùng (Persona) và dự đoán ý định mua hàng (Purchase Intent) sử dụng Deep Learning (Adam Optimizer).
2. **Graph RAG**: Xây dựng Knowledge Graph từ 15k+ tương tác người dùng trên Neo4j để đưa ra gợi ý sản phẩm cá nhân hóa.
3. **Text RAG**: Hệ thống tư vấn khách hàng dựa trên tài liệu (KBStore) sử dụng TF-IDF & Cosine Similarity.
4. **Auto-Sync**: Webhook tự động đồng bộ sản phẩm mới từ Catalog sang Knowledge Graph.

---

## Cách chạy

### Khởi động hệ thống
```bash
docker-compose up -d --build
```

### Chạy AI Training & Graph Build
```bash
# Huấn luyện Deep Learning (Persona, Intent)
docker exec shopx-ai_service python manage.py train_behavior

# Xây dựng đồ thị Neo4j
docker exec shopx-ai_service python ai_pipeline/build_kb_graph.py
```

### Seed dữ liệu Catalog
```bash
python scripts/seed_data.py
```

---

## URLs quan trọng

| Trang               | URL                              |
|---------------------|----------------------------------|
| Frontend            | http://localhost:4000            |
| API Gateway         | http://localhost:8000            |
| Neo4j Browser       | http://localhost:7474            |
| RabbitMQ Management | http://localhost:15672           |

---

## Tài liệu chi tiết
- [Kiến trúc chi tiết](docs/agent-docs/ARCHITECTURE.md)
- [Báo cáo AI Service](docs/agent-docs/AI_SERVICE_ASSIGNMENT_REPORT.md)
