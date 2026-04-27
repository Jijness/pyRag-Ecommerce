# CONTINUE.MD – Ngữ cảnh tiếp tục phiên làm việc

**Cập nhật:** 27/04/2026 – Đã hoàn thành toàn bộ
**Deadline nộp tiểu luận:** 23h30 tối nay  
**Mục tiêu:** 100% (8/8) microservices đã được chuyển đổi thành công từ FastAPI → Django REST Framework. Hệ thống hoạt động trơn tru.

---

## ✅ ĐÃ HOÀN THÀNH (KHÔNG CẦN SỬA LẠI)

| Service | Port | Framework | Ghi chú |
|---------|------|-----------|---------|
| `auth_service` | 8001 | Django+DRF | ✅ Xong từ trước |
| `product_service` | 8002 | Django+DRF | ✅ Xong + RAG webhook `trigger_ai_sync()` |
| `order_service` | 8003 | Django+DRF | ✅ Xong – commit `8c8ddbd` – đã push GitHub |

**Các việc khác đã xong:**
- Fix nút "Đặt hàng ngay" (đã xóa `innerHTML.replace()` phá DOM event listeners trong `frontend/app.js`)
- RAG Auto-sync: `product_service` → `POST /sync-product` → `ai_chat_service` → `upsert_product()` vào Neo4j (✅ **Đã kiểm chứng**: `ProductViewSet` trong `catalog/views.py` đã override `perform_create` và `perform_update` để gọi `trigger_ai_sync()`. Luồng sync tự động khi nhân viên (staff) thêm/sửa sản phẩm hoạt động đúng như yêu cầu, chỉ sync thông tin catalog thay vì dữ liệu tương tác).
- Viết lại `README.md`, `docs/agent-docs/ARCHITECTURE.md`, `docs/agent-docs/DJANGO_MIGRATION_GUIDE.md`

---

## ✅ ĐÃ HOÀN THÀNH - TẤT CẢ 8 SERVICES

| Service | Port | Framework | Trạng thái |
|---------|------|-----------|---------|
| `customer_service` | 8004 | Django+DRF | ✅ Đã migrate & test OK |
| `staff_service` | 8005 | Django+DRF | ✅ Đã migrate & test OK |
| `marketing_service` | 8006 | Django+DRF | ✅ Đã migrate & test OK |
| `inventory_service` | 8007 | Django+DRF | ✅ Đã migrate & test OK |
| `content_service` | 8008 | Django+DRF | ✅ Đã migrate & test OK |
| `interaction_service` | 8009 | Django+DRF | ✅ Đã migrate & test OK |
| `analytics_service` | 8010 | Django+DRF | ✅ Đã migrate & test OK |
| `notification_service` | 8011 | Django+DRF | ✅ Đã migrate & test OK |

Tất cả đã được cấu hình trong `docker-compose.yml`, sử dụng `python manage.py runserver`, database migrations thành công, và vượt qua health check test.

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
