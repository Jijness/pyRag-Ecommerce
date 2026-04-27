# DDD Refactor Notes

## Nguyên tắc áp dụng (Chuẩn Tiểu Luận Chương 2)
- Hệ thống sử dụng kiến trúc lai: Các service lõi (`auth_service`, `product_service`) bắt buộc dùng **Django + DRF**. Các service khác có thể giữ FastAPI.
- Một `product_service` duy nhất cho toàn bộ catalog.
- Không tách service theo category. Category chỉ là dữ liệu.
- `product_service` được tổ chức theo các lớp `domain`, `application`, `infrastructure`, `presentation` (chuẩn DDD).
- **Thiết kế Model:** Dùng 1 bảng `Product` duy nhất. Các thuộc tính khác biệt của >10 loại sản phẩm (Sách, Điện thoại, Áo...) được lưu trong cột `attributes` (JSONB) thay vì dùng Inheritance.

## Danh mục mới
- Sách
- Dụng cụ học tập
- Đồ chơi
- Gói quà

## Thay đổi chính
- `book_service` được thay bằng `product_service` trong `docker-compose.yml`.
- API gateway map `/products/*` vào `product_service`.
- Frontend chuyển route chính sang `#/products`.
- AI chatbot chuyển từ gợi ý sách sang gợi ý sản phẩm marketplace.
- Seed dữ liệu demo dùng tài khoản `demo@learnmart.vn / demo123`.

## Product service structure (Django)
```text
product_service/
  manage.py
  config/
    settings.py
    urls.py
  modules/
    catalog/
      domain/
        entities/
          product.py (chứa JSON attributes)
          category.py
      application/
        services/
      infrastructure/
        models/
          product_model.py
          category_model.py
        migrations/
      presentation/
        api/
          views/
          serializers/
      seeds/
```
