# Django Migration Guide – ShopX Marketplace

Tài liệu này ghi lại quá trình chuyển đổi từ **FastAPI** sang **Django REST Framework** cho các core service của ShopX.

---

## Trạng thái Migration (cập nhật 27/04/2026)

| Service             | Framework cũ | Framework mới | Trạng thái |
|---------------------|-------------|---------------|------------|
| `auth_service`      | FastAPI     | **Django+DRF**| ✅ Hoàn thành |
| `product_service`   | FastAPI     | **Django+DRF**| ✅ Hoàn thành |
| `order_service`     | FastAPI     | **Django+DRF**| ✅ Hoàn thành (27/04/2026) |
| `customer_service`  | FastAPI     | FastAPI       | ⏳ Chưa migrate |
| `staff_service`     | FastAPI     | FastAPI       | ⏳ Chưa migrate |
| `marketing_service` | FastAPI     | FastAPI       | ⏳ Chưa migrate |
| `inventory_service` | FastAPI     | FastAPI       | ⏳ Chưa migrate |
| `ai_chat_service`   | FastAPI     | FastAPI       | 🔒 Giữ nguyên (AI pipeline) |
| `behavior_service`  | FastAPI     | FastAPI       | 🔒 Giữ nguyên (AI pipeline) |

---

## Order Service – Cấu trúc Django mới

### Cấu trúc thư mục

```
order_service/
├── config/
│   ├── settings.py     # Parse DATABASE_URL tự động
│   ├── urls.py         # Root URL router
│   ├── wsgi.py
│   └── asgi.py
├── cart/               # Django App – Bounded Context: Cart
│   ├── models.py       # Cart, CartItem
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── orders/             # Django App – Bounded Context: Order
│   ├── models.py       # Order, OrderItem
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── payment/            # Django App – Bounded Context: Payment
│   ├── models.py       # Payment, Refund
│   └── ...
├── shipping/           # Django App – Bounded Context: Shipping
│   ├── models.py       # Shipping
│   └── ...
└── manage.py
```

### API Endpoints (tương đương FastAPI cũ)

| Endpoint                                    | Method | Mô tả                    |
|---------------------------------------------|--------|--------------------------|
| `/health`                                   | GET    | Health check             |
| `/cart/{cid}`                               | GET    | Xem giỏ hàng             |
| `/cart/{cid}/add`                           | POST   | Thêm vào giỏ             |
| `/cart/{cid}/item/{id}/quantity`            | PATCH  | Cập nhật số lượng        |
| `/cart/{cid}/item/{id}`                     | DELETE | Xóa sản phẩm khỏi giỏ   |
| `/cart/{cid}/clear`                         | DELETE | Xóa toàn bộ giỏ          |
| `/cart/{cid}/summary`                       | GET    | Tóm tắt giỏ hàng         |
| `/orders/checkout`                          | POST   | Đặt hàng từ giỏ          |
| `/orders/customer/{cid}`                    | GET    | Lịch sử đơn hàng         |
| `/orders/{id}`                              | GET    | Chi tiết đơn hàng        |
| `/orders/{id}/items`                        | GET    | Danh sách sản phẩm       |
| `/orders/{id}/status`                       | PATCH  | Cập nhật trạng thái      |
| `/orders/stats/summary`                     | GET    | Thống kê                 |

### Luồng Checkout

```python
POST /orders/checkout
Body: {
  "customer_id": 1,
  "ship_method": "standard",   # standard (15k) | fast (30k)
  "pay_method": "COD",         # COD | BANKING | MOMO
  "coupon_code": "SALE20",     # Optional
  "note": "..."                # Optional
}
```

**Quy trình:**
1. Lấy giỏ hàng active của customer
2. Tính `total_price + shipping_fee`
3. Tạo `Order` (status=PENDING)
4. Tạo `OrderItem` cho từng sản phẩm trong giỏ
5. Tạo `Shipping` (status=PENDING)
6. Tạo `Payment` (status=Pending)
7. Deactivate giỏ hàng (`cart.is_active = False`)

---

## Product Service – RAG Auto-sync Webhook

Khi Staff tạo/sửa sản phẩm, `ProductViewSet` sẽ tự động gọi:

```python
def trigger_ai_sync(self, product):
    payload = {
        "id": product.id,
        "title": product.name,
        "price": float(product.price),
        "category_name": product.category.name,
        "brand_name": "ShopX",
        "description": product.description
    }
    httpx.post("http://ai_chat_service:8012/sync-product", json=payload)
```

**AI Chat Service nhận tại:**

```python
@app.post("/sync-product")
def sync_product(body: ProductSyncRequest) -> dict:
    advisor.graph.upsert_product(body.dict())
    return {"status": "ok", "product_id": body.id}
```

**Graph Store thực hiện:**

```cypher
MERGE (p:Product {id: $product_id})
SET p.title = $title, p.price = $price, ...
MERGE (c:Category {name: $category_name})
MERGE (p)-[:BELONGS_TO]->(c)
```

---

## Notes quan trọng khi migrate

1. **DATABASE_URL parsing:** Settings.py tự động parse `DATABASE_URL` từ môi trường Docker để lấy đúng password.
2. **Fake Initial Migration:** Vì bảng đã tồn tại từ FastAPI/SQLAlchemy, dùng `manage.py migrate --fake-initial` thay vì `migrate` bình thường.
3. **Field mapping:** `book_id` trong model cũ → vẫn giữ tên `book_id` trong Django model để tương thích DB. Frontend map sang `product_id` qua API layer.
