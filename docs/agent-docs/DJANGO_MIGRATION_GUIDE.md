# CẢNH BÁO KIẾN TRÚC LAI (DJANGO + FASTAPI)

Tài liệu này dành cho các AI Agent hoặc Lập trình viên tiếp nhận dự án ở các giai đoạn sau.

## 1. Tình trạng hệ thống hiện tại (Tháng 04/2026)
Hệ thống ban đầu được code 100% bằng **FastAPI + SQLAlchemy**. Tuy nhiên, để đáp ứng yêu cầu chấm điểm của "Tiểu luận Môn học Kiến trúc Phần mềm" (Chương 2), một số service cốt lõi bắt buộc phải chuyển sang **Django + Django REST Framework (DRF)**.

**Phân bổ Framework hiện tại:**
- 🔴 **`auth_service`**: Đã/Đang chuyển sang **Django**. Sử dụng AbstractUser, DRF SimpleJWT.
- 🔴 **`product_service`**: Đã/Đang chuyển sang **Django**. Chú ý: Sử dụng `models.JSONField()` cho cột `attributes` để xử lý >10 loại sản phẩm khác nhau.
- 🟡 **Các service khác (Order, Cart...)**: Sẽ được chuyển dần sang Django.
- 🟢 **`ai_chat_service` & `ai_pipeline`**: **TUYỆT ĐỐI GIỮ NGUYÊN FASTAPI & THUẦN PYTHON**. Không được phép chuyển các thư mục này sang Django vì chứa logic Machine Learning và RAG nội bộ rất phức tạp.

## 2. Quy tắc cho AI Agent
1. **Kiểm tra file `.bak.py`**: Khi vào thư mục một service, nếu thấy có file `app.py.bak` hoặc `main.py.bak`, điều đó có nghĩa là service này vừa được chuyển từ FastAPI sang Django. KHÔNG XÓA các file `.bak` trừ khi có lệnh trực tiếp từ User.
2. **Database Clean-up**: Với các service Django không dùng xác thực (như Product, Order), phải đảm bảo file `settings.py` ĐÃ TẮT `django.contrib.auth`, `django.contrib.admin`, `django.contrib.sessions` để không sinh ra bảng rác trong database của Microservice đó.
3. **Product Domain**: Đọc kỹ phần `attributes = models.JSONField()` trong `product_model.py`. Hệ thống không dùng kế thừa (Inheritance) cho Book, Electronics... mà dùng Entity-Attribute-Value pattern thông qua JSONB để tuân thủ DDD.

## 3. Lịch sử Migration
- Code FastAPI gốc: Đang chạy tốt ở các port 800x.
- Đang thực hiện refactor (theo DDD_REFACTOR_NOTES.md) kết hợp chuyển framework.
