# CONTINUE.MD – Ngữ cảnh tiếp tục phiên làm việc

**Cập nhật:** 27/04/2026 – 18:37  
**Deadline nộp tiểu luận:** 23h30 tối nay  
**Mục tiêu còn lại:** Hoàn tất migrate 7 service từ FastAPI → Django REST Framework

---

## ✅ ĐÃ HOÀN THÀNH (KHÔNG CẦN SỬA LẠI)

| Service | Port | Framework | Ghi chú |
|---------|------|-----------|---------|
| `auth_service` | 8001 | Django+DRF | ✅ Xong từ trước |
| `product_service` | 8002 | Django+DRF | ✅ Xong + RAG webhook `trigger_ai_sync()` |
| `order_service` | 8003 | Django+DRF | ✅ Xong – commit `8c8ddbd` – đã push GitHub |

**Các việc khác đã xong:**
- Fix nút "Đặt hàng ngay" (đã xóa `innerHTML.replace()` phá DOM event listeners trong `frontend/app.js`)
- RAG Auto-sync: `product_service` → `POST /sync-product` → `ai_chat_service` → `upsert_product()` vào Neo4j (nhưng đầu việc này vẫn cần check lại là thực sự đã hoàn thành luồng sync tự đọng khi nhân viên thêm/sửa sản phẩm hay mới chỉ đang sync dữ liệu tương tác của người dùng customer mà thôi? à mà staff thì ko cần phải thu thập dữ liệu tương tác sử dụng hệ thống để phục vụ đề xuất và chatbot nhé, nhân viên chỉ cần track được cái thay đổi thêm sản phẩm mới là được)
- Viết lại `README.md`, `docs/agent-docs/ARCHITECTURE.md`, `docs/agent-docs/DJANGO_MIGRATION_GUIDE.md`

---

## 🔶 ĐANG LÀM DỞ – `customer_service` (port 8004)

**Code đã viết (chưa Docker test, chưa commit):**
- ✅ `config/settings.py` – parse DATABASE_URL
- ✅ `customers/models.py` – CustomerProfile, Address, Wishlist, WishlistItem, Newsletter, CustomerPreference
- ✅ `customers/views.py` – tất cả API views
- ✅ `customers/urls.py` – URL patterns

**CÒN THIẾU (phải làm khi mở lại):**
1. Tạo `config/urls.py` (root URL router include customers.urls)
2. Sửa `Dockerfile`: đổi CMD từ uvicorn → `python manage.py runserver 0.0.0.0:8004`
3. Viết lại `requirements.txt` (thêm django, djangorestframework, pymysql)
4. Sửa `docker-compose.yml`: đổi command của `customer_service`
5. Build & up: `docker-compose build customer_service ; docker-compose up -d customer_service`
6. Migrate: `docker-compose exec -T customer_service python manage.py makemigrations customers ; docker-compose exec -T customer_service python manage.py migrate --fake-initial`

---

## 🔴 CHƯA LÀM – 7 SERVICE CÒN LẠI

### 1. `staff_service` (port 8005) – DB: `staff_db`
**Models FastAPI:**
- `StaffProfile` (staff_id, full_name, role, department_id, phone, avatar_url, hire_date, is_active)
- `Department` (name, description, manager_id)

**API giữ nguyên:**
- `GET /profile/{staff_id}`, `PUT /profile/{staff_id}`, `POST /profile`
- `GET /departments`, `POST /departments`
- `GET /health`

---

### 2. `marketing_service` (port 8006) – DB: `marketing_db` ⚠️ QUAN TRỌNG (dùng trong RAG)
**Models FastAPI:**
- `Coupon` (code, discount_percent, discount_amount, min_order_value, max_uses, used_count, valid_from, valid_to, active)
- `Promotion` (name, description, discount_percent, start_date, end_date, is_active)
- `MembershipTier` (name, min_points, discount_percent, free_shipping, description)
- `FlashSale` (name, discount_percent, max_quantity, sold_quantity, start_at, end_at, product_id, is_active)
- `ReferralCode` (code, owner_customer_id, reward_points, is_active, used_count, created_at)
- `Bundle` (name, price, description, is_active)
- `Discount` (name, product_id, genre_id, discount_percent, start_date, end_date, is_active)

**API giữ nguyên (critical cho RAG graph):**
- `GET /coupons`, `POST /coupons`
- `GET /coupons/validate/{code}?order_total=XXX`
- `GET /promotions`, `POST /promotions`
- `GET /flash-sales`, `POST /flash-sales`
- `GET /tiers`, `POST /tiers/seed` (seed 4 tier Bronze/Silver/Gold/Platinum)
- `POST /referrals/{cid}` (tạo referral code cho customer)
- `GET /health`

---

### 3. `inventory_service` (port 8007) – DB: `inventory_db`
**Models FastAPI:**
- `Warehouse` (name, location, capacity, current_stock)
- `Supplier` (name, contact_name, email, phone, address, is_active)
- `PurchaseOrder` (supplier_id, product_id, quantity, unit_cost, status, ordered_at, received_at)
- `InventoryAlert` (product_id, alert_type, threshold, current_stock, message, is_resolved, created_at)

**API giữ nguyên:**
- `GET /warehouses`, `POST /warehouses`
- `GET /suppliers`, `POST /suppliers`
- `GET /alerts`, `POST /alerts`
- `GET /health`

---

### 4. `content_service` (port 8008) – DB: `content_db`
**Models FastAPI:**
- `Banner` (title, image_url, link_url, is_active, display_order)
- `Collection` (name, description, product_ids JSON, is_active)
- `BlogPost` (title, content, author, published_at, is_published, tags)

**API giữ nguyên:**
- `GET /banners`, `POST /banners`
- `GET /collections`, `POST /collections`
- `GET /blog`, `POST /blog`
- `GET /health`

---

### 5. `interaction_service` (port 8009) – DB: `interaction_db`
**Models FastAPI:**
- `LoyaltyPoints` (customer_id, points, tier, last_updated)
- `GiftCard` (code, amount, remaining_amount, issued_to, is_active, expires_at)

**API giữ nguyên:**
- `GET /loyalty-points/{cid}`
- `GET /gift-cards/{code}`, `POST /gift-cards`
- `GET /health`

---

### 6. `analytics_service` (port 8010) – DB: `analytics_db`
**Models FastAPI:**
- `SalesSummary` (date, total_orders, total_revenue, avg_order_value, top_product_id)
- `SearchHistory` (customer_id, query, searched_at, result_count)
- `RecentlyViewed` (customer_id, product_id, viewed_at)

**API giữ nguyên:**
- `GET /sales`
- `POST /search-history`, `GET /recently-viewed/{cid}`, `POST /recently-viewed`
- `GET /health`

---

### 7. `notification_service` (port 8011) – DB: `notification_db`
**Models FastAPI:**
- `Notification` (customer_id, title, message, is_read, created_at, notification_type)

**API giữ nguyên:**
- `GET /notifications/{cid}`
- `POST /notifications`
- `PATCH /notifications/{id}/read`
- `GET /health`

---

## 📋 QUY TRÌNH CHUẨN CHO MỖI SERVICE

```python
# TEMPLATE settings.py (copy từ order_service, đổi tên DB và secret key)
# Key points:
# - INSTALLED_APPS: chỉ cần contenttypes, auth, rest_framework, <appname>
# - Đoạn parse DATABASE_URL bằng regex (PHẢI có để đọc đúng password)
# - REST_FRAMEWORK AllowAny + JSONRenderer + UNAUTHENTICATED_USER=None
```

```bash
# Powershell – dùng ";" thay "&&"
docker-compose build <svc> ; docker-compose up -d <svc>
docker-compose exec -T <svc> python manage.py migrate --fake-initial
```

**Checklist từng service:**
- [ ] `config/settings.py` – parse DATABASE_URL
- [ ] `<app>/models.py` – giữ `db_table` khớp tên bảng MySQL cũ  
- [ ] `<app>/views.py` – views tương đương FastAPI (dùng `@api_view`)
- [ ] `<app>/urls.py` – URL patterns khớp endpoint cũ
- [ ] `config/urls.py` – root router include app urls + `/health`
- [ ] `Dockerfile` – đổi CMD: `python manage.py runserver 0.0.0.0:<port>`
- [ ] `requirements.txt` – ghi bằng `write_to_file` (tránh UTF-16 encoding lỗi)
  ```
  django
  djangorestframework
  pymysql
  cryptography
  ```
- [ ] `docker-compose.yml` – đổi `command:` của service (bỏ RABBITMQ_URL nếu ko dùng)
- [ ] Build & up
- [ ] `migrate --fake-initial`
- [ ] Test: `Invoke-WebRequest http://localhost:<port>/health`

---

## ⚙️ LƯU Ý KỸ THUẬT KHI THỰC HIỆN CHUYỂN ĐỔI

1. **Giữ tên bảng:** `class Meta: db_table = 'tên_bảng_cũ'` – tránh mất dữ liệu MySQL hiện có
2. **book_id vs product_id:** Model giữ `book_id`, serializer expose thêm `product_id` alias
3. **Powershell:** dùng `;` không dùng `&&`
4. **requirements.txt:** Dùng `write_to_file` với `Overwrite=true` – KHÔNG dùng `echo >>` (bị UTF-16)
5. **Fake migrate:** Bảng đã tồn tại → luôn dùng `--fake-initial`
6. **Docker tắt:** Viết code xong hết rồi mới build 1 lần cho nhanh, thực hiện việc check và kiểm tra sau khi hoàn tất cx đc. 

---

## 🗂️ FILES THAM KHẢO (KHÔNG SỬA)

- Settings chuẩn: `backend-services/order_service/config/settings.py`
- Dockerfile chuẩn: `backend-services/order_service/Dockerfile`  
- Views pattern: `backend-services/order_service/cart/views.py`
- Docker-compose entry mẫu: xem section `order_service` trong `docker-compose.yml`
- Customer service (đang dở): `backend-services/customer_service/`
