# AI Service Context — Thiết Kế Chi Tiết

**Service:** `ai_service` | **Port:** 8007 | **Database:** `ai_db` (MySQL) + Neo4j (Knowledge Graph)

---

## 1. Mô Tả Bounded Context

AI Service là context thông minh tổng hợp — nơi hội tụ toàn bộ pipeline thu thập hành vi người dùng, huấn luyện model, và suy diễn trả về đề xuất cá nhân hóa. Đây là Bounded Context phức tạp nhất trong hệ thống vì nó **kết hợp 3 paradigm kỹ thuật**:

1. **Behavior Tracking** — Thu thập mọi tương tác của người dùng (click, search, wishlist, buy)
2. **Knowledge Graph (Neo4j)** — Đồ thị quan hệ Người dùng ↔ Sản phẩm ↔ Danh mục
3. **RAG (Retrieval-Augmented Generation)** — Chatbot tư vấn kết hợp vector search + LLM

> [!IMPORTANT]
> **Framework:** Phải migrate từ FastAPI sang **Django + DRF**. Giữ nguyên toàn bộ business logic (Neo4j sync, LSTM feature compute, RAG pipeline), chỉ bọc lại bằng Django Views.

---

## 2. Actors & Use Cases

### Actors:
- **Customer** — Người dùng tương tác với chatbot, nhận đề xuất sản phẩm
- **Guest** — Duyệt sản phẩm (hành vi ẩn danh vẫn được track qua session_id)
- **Staff / Admin** — Xem analytics, báo cáo hành vi
- **Product Service** — Publish event `product.synced` để sync sang Neo4j
- **Frontend** — Gửi behavior events qua API

### Use Case Tổng Quan:
```
[AI Service Context]
    │
    ├── UC01: Hỏi chatbot tư vấn sản phẩm ──────── Customer
    ├── UC02: Nhận đề xuất sản phẩm cá nhân hóa ──── Customer
    ├── UC03: Quản lý Wishlist ─────────────────── Customer
    ├── UC04: Xem hoạt động cá nhân ───────────── Customer
    ├── UC05: Xem báo cáo analytics ───────────── Admin
    └── UC06: Đồng bộ sản phẩm vào Knowledge Graph ─ Product Service

[Hệ thống tự động - không phải UC riêng]:
    - Ghi nhận BehaviorEvent khi Customer thực hiện hành động khác
    - Cập nhật CustomerBehaviorProfile sau mỗi event
    - Sync Neo4j sau mỗi product.synced event
```

| UC | Tên | Actor | Mô tả ngắn |
|---|---|---|---|
| UC01 | Chatbot | Customer | Gửi câu hỏi → RAG retrieval + LLM → trả lời + top sản phẩm |
| UC02 | Đề xuất SP | Customer | GET /recommend → Neo4j + behavior profile → danh sách đề xuất |
| UC03 | Quản lý Wishlist | Customer | Thêm/xóa/xem sản phẩm yêu thích; hệ thống tự ghi BehaviorEvent |
| UC04 | Hoạt động cá nhân | Customer | Xem lịch sử tìm kiếm, sản phẩm đã xem, behavior profile |
| UC05 | Analytics | Admin | Xem DailySalesSummary, top searches, behavior stats |
| UC06 | Neo4j sync | Product Service | Consume `product.synced` → upsert Product node trong Neo4j |

---

## 3. Entities & Attributes

### 3.1 `BehaviorEvent` — Entity (Aggregate Root của tracking)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_id | int (nullable) | Null nếu Guest |
| session_id | string (nullable) | Cho Guest tracking |
| event_type | string | search_performed / product_viewed / wishlist_added / cart_added / checkout_started / order_completed |
| product_id | int (nullable) | Soft ref → Product |
| category_name | string (nullable) | Snapshot tên danh mục |
| query | string (nullable) | Từ khóa tìm kiếm |
| price | float (nullable) | Giá sản phẩm lúc xem |
| quantity | int (nullable) | |
| source | string (nullable) | search / recommend / direct |
| metadata | JSONField | Dữ liệu bổ sung |
| occurred_at | datetime | |

### 3.2 `CustomerBehaviorProfile` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_id | int (unique) | Soft ref → User |
| persona | string | new_explorer / deal_hunter / high_intent_buyer / loyal_member / category_browser |
| price_sensitivity | string | high / medium / low |
| purchase_intent | float (0–1) | Điểm ý định mua |
| preferred_categories | JSONField | Top 3 danh mục yêu thích |
| next_best_action | string | recommend_entry / push_coupon / upsell_membership / bundle_related |
| feature_values | JSONField | {search_count, view_count, order_count, ...} |
| summary | text | |
| last_event_at | datetime | |
| updated_at | datetime | |

### 3.3 `Wishlist` — Entity (chuyển từ customer_service)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_id | int | Soft ref → User |
| created_at | datetime | |

### 3.4 `WishlistItem` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| wishlist_id | int (FK → Wishlist) | |
| product_id | int | Soft ref → Product |
| added_at | datetime | |

### 3.5 `CustomerPreference` — Entity (chuyển từ customer_service)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_id | int (unique) | Soft ref → User |
| favorite_categories | JSONField | |
| preferred_language | string | |
| notification_enabled | boolean | |

### 3.6 `SearchHistory` — Entity (từ analytics_service)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_id | int | |
| query | string | |
| result_count | int | |
| searched_at | datetime | |

### 3.7 `RecentlyViewed` — Entity (từ analytics_service)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_id | int | |
| product_id | int | Soft ref → Product |
| product_title | string | Snapshot tên SP |
| viewed_at | datetime | |

### 3.8 `DailySalesSummary` — Entity (từ analytics_service)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| date | date (unique) | |
| total_orders | int | |
| total_revenue | float | |
| top_product_ids | JSONField | |

---

## 4. Neo4j Knowledge Graph Schema

```
Nodes:
  (:User   {id, persona, membership_tier})
  (:Product {id, name, category, price})
  (:Category {name})

Edges:
  (:User)-[:VIEWED {count, last_at}]→(:Product)
  (:User)-[:BOUGHT {count, total_spent}]→(:Product)
  (:User)-[:WISHLISTED]→(:Product)
  (:User)-[:SEARCHED {query}]→(:Category)
  (:Product)-[:BELONGS_TO]→(:Category)
  (:Product)-[:SIMILAR_TO {score}]→(:Product)
```

**Cypher Query mẫu (gợi ý sản phẩm):**
```cypher
MATCH (u:User {id: $customer_id})-[:VIEWED|BOUGHT]→(p:Product)
→(similar:Product)
WHERE NOT (u)-[:BOUGHT]→(similar)
RETURN similar.id, similar.name, count(*) as score
ORDER BY score DESC LIMIT 10
```

---

## 5. Pipeline AI

### 5.1 Behavior Collection Pipeline
```
Frontend/User action
    → POST /ai/behavior/events (BehaviorEvent)
    → Graph Sync: Upsert Neo4j node/edge
    → Recompute CustomerBehaviorProfile (LSTM feature extraction)
    → Save CustomerBehaviorProfile
```

### 5.2 Recommendation Pipeline
```
Customer → GET /ai/recommend?customer_id=123
    → Get CustomerBehaviorProfile (persona, preferred_categories)
    → Query Neo4j: Collaborative filtering (đồng loại + tương tự)
    → Filter by CustomerPreference
    → Rank by purchase_intent × product_score
    → Return top 10 products
```

### 5.3 RAG Chatbot Pipeline
```
Customer → POST /ai/chat
  Body: { message: "Tôi muốn mua laptop gaming dưới 20 triệu" }

  Step 1: User Snapshot (REST calls)
    → GET user_service /users/me → profile, membership_tier
    → GET /ai/behavior/profile/{id} → persona, preferred_categories
    → GET /ai/wishlist/{id} → wishlist items
    → GET /ai/recently-viewed/{id} → recent products

  Step 2: RAG Retrieval
    → Embed query → vector similarity search (knowledge base docs)
    → Top K chunks retrieved

  Step 3: Knowledge Graph context
    → Cypher query → relevant products from Neo4j

  Step 4: LLM Generation
    → Compose prompt: [system] + [user_snapshot] + [rag_context] + [kg_context] + [message]
    → LLM generate response

  Step 5: Return
    → { answer, recommended_products, reasoning }
```

### 5.4 Product Sync (Webhook / RabbitMQ)
```
[RabbitMQ] product.synced event received
    → Parse: product_id, name, category, price, description
    → Upsert Product node in Neo4j
    → Create/update BELONGS_TO edge to Category node
    → Update knowledge base chunk (if description changed)
```

---

## 6. Relationships

| Quan hệ | Từ | Đến | Loại | Cardinality |
|---|---|---|---|---|
| Composition | Wishlist | WishlistItem | has-parts (cascade delete) | 1..1 → 0..* |
| Association | CustomerBehaviorProfile | BehaviorEvent | aggregates | 1..1 → 0..* |
| Association (Logical) | BehaviorEvent | Customer (User Context) | by ID | 0..* → 0..1 |
| Association (Logical) | BehaviorEvent | Product (Product Context) | by ID | 0..* → 0..1 |
| Association (Logical) | Wishlist | Customer (User Context) | by ID | 0..* → 1..1 |
| Association (Logical) | WishlistItem | Product (Product Context) | by ID | 0..* → 1..1 |

---

## 7. API Endpoints Chính

| Method | Endpoint | Actor | Mô tả |
|---|---|---|---|
| POST | `/ai/chat` | Customer | Gửi câu hỏi chatbot |
| GET | `/ai/recommend` | Customer | Đề xuất sản phẩm cá nhân hóa |
| POST | `/ai/behavior/events` | Frontend | Ghi nhận hành vi |
| GET | `/ai/behavior/events/{customer_id}` | Customer | Xem lịch sử events |
| GET | `/ai/behavior/profile/{customer_id}` | Customer/Admin | Xem BehaviorProfile |
| POST | `/ai/behavior/profile/{customer_id}/refresh` | System/Customer | Tính lại profile |
| GET | `/ai/wishlist/{customer_id}` | Customer | Xem wishlist |
| POST | `/ai/wishlist/items` | Customer | Thêm vào wishlist |
| DELETE | `/ai/wishlist/items/{id}` | Customer | Xóa khỏi wishlist |
| GET | `/ai/recently-viewed/{customer_id}` | Customer | Sản phẩm đã xem gần đây |
| GET | `/ai/search-history/{customer_id}` | Customer | Lịch sử tìm kiếm |
| GET | `/ai/analytics/summary` | Admin | Báo cáo doanh thu theo ngày |

---

## 8. Django Apps Nội Bộ

```
ai_service/
├── behavior/       ← BehaviorEvent, CustomerBehaviorProfile + Neo4j sync logic
├── analytics/      ← SearchHistory, RecentlyViewed, DailySalesSummary
├── wishlist/       ← Wishlist, WishlistItem, CustomerPreference
├── chatbot/        ← RAG pipeline, LLM inference
└── recommendation/ ← Neo4j Cypher queries, ranking logic
```

## 9. Ghi Chú Migration

- Source code chính: `backend-services/ai_service/` + `backend-services/behavior_service/`
- Framework: **FastAPI → Django + DRF** (giữ nguyên business logic)
- Di chuyển: `Wishlist`, `WishlistItem`, `CustomerPreference` từ `customer_service`
- Di chuyển: `SearchHistory`, `RecentlyViewed`, `DailySalesSummary` từ `analytics_service`
- Database mới: `ai_db` (merge từ `behavior_db` + `analytics_db`)
- Neo4j: Giữ nguyên `shopx-neo4j`, chỉ cập nhật connection config
- Rename folder: `ai_service/` → `ai_service/`
