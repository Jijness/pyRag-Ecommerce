# Docker Compose & Architecture Guidelines

Bộ quy tắc này quy định tiêu chuẩn viết và thiết lập `docker-compose.yml` cho các vi dịch vụ (microservices), đảm bảo môi trường phát triển (Development) luôn ổn định, không bị xung đột khi chạy song song nhiều dự án khác nhau trên cùng một máy chủ.

## 1. QUY TẮC VỀ VOLUME (DỮ LIỆU DATABASE)
- **Tuyệt đối** không dùng volume mặc định do Docker tự sinh hoặc dùng chung volume giữa các project.
- **Quy tắc Đặt tên:** Mọi volume phải có tiền tố là tên viết tắt của project kết hợp tên service để tránh xung đột hệ thống.
  - *Ví dụ đúng:* `mprj-identity-db-data`, `mprj-booking-db-data`.
- Volume phải được khai báo rõ ràng ở mục `volumes:` ở cuối file cấu hình.
- **Mục tiêu:** Không bị ghi đè database giữa các dự án môn học/công ty; dữ liệu được bảo toàn nguyên vẹn ngay cả khi switch project hoặc restart Docker.

## 2. QUY TẮC VỀ PORT (CỔNG KẾT NỐI)
- Cổng của các Database trỏ trực tiếp ra Host Server nên được tịnh tiến độc quyền và quản lý dễ dàng (Ví dụ: `3307:3306`, `3308:3306`).
- **Nghiêm cấm** để nhiều service database ở các project khác nhau trùng port binding ra Host.
- **Workflow:** Luôn tập thói quen chạy `docker compose down` trước khi chuyển sang chạy project khác để triệt tiêu mọi cổng đang được giữ.

## 3. QUY TẮC VỀ AUTH ENVS (USERNAME / PASSWORD)
- Các microservice trong cùng 1 project nên dùng chung một `MYSQL_ROOT_PASSWORD` để dễ liên kết test (hoặc tuân theo cơ chế bảo mật nội bộ tương đương).
- Password **không được hardcode lộ liễu**. Phải quản lý thông qua biến môi trường hoặc file `.env`.
  - *Cú pháp ưu tiên:* `MYSQL_ROOT_PASSWORD: ${DB_PASSWORD:-123456}` (Ưu tiên đọc file `.env`, nếu không có sẽ tự động lùi về pass `123456`).
- **Mục tiêu:** Dễ dàng kết nối từ MySQL Workbench hoặc DBeaver; chuyển project từ máy người này sang người khác không bị crash do sai thông tin đăng nhập.

## 4. QUY TẮC ĐỊNH DANH CONTAINER NAME
- Bắt buộc phải khai báo bằng cờ `container_name:` ở mọi dịch vụ được định nghĩa.
- **Syntax Prefix:** Tên container bắt buộc phải mang prefix của dự án để tránh xung đột tên.
  - *Ví dụ:* `container_name: mprj-identity-mysql`, `container_name: mprj-identity-service`.
- Không được để Docker tự sinh tên tự động (vì nó sẽ sinh ra dạng `folder-service-1` dễ cấn với các folder khác hệ thống).

## 5. QUY TẮC RESTART POLICY
- Trong môi trường Development (Code local), bắt buộc đặt: `restart: "no"`.
- **Tuyệt đối không dùng** `always` hoặc `unless-stopped` khi code.
- **Mục tiêu:** Tránh việc Docker nén toàn bộ tài nguyên tự động khởi chạy lại toàn bộ microservices mỗi khi máy tính bật lên, gây hao hụt RAM và xung đột ngầm.

## 6. QUY TẮC CLEAN ARCHITECTURE TRONG DOCKER
- Thiết kế phân liệt rõ ràng: Database Service 1 cụm, Application Service 1 cụm. Cụm nào đi với mạng đính kèm của cụm đó.
- Cụm Application phải ràng buộc theo Cụm Database bằng `depends_on`.
- Bắt buộc xài cấu trúc **Healthcheck** để đảm bảo Cụm DB hoàn toàn khởi chạy xong (Ping Pass) thì Cụm App mới được phép Boot. (*Service Database bị sập sẽ cấm việc Service App ngoi lên vô ích*).

## 7. ĐIỀU LỆ TỔNG QUÁT (TÓM GỌN LẠI)
1. Cấm dùng tên Volume vô danh (Anonymous volume).
2. Cấm Host Port Mapping trùng lặp.
3. Cấm Container Name vô danh.
4. Ưu tiên cấp phát Auth bằng `.env`.
5. Luôn `docker compose down` sau khi ngưng làm việc.
6. Thiết kế module phải dễ bảo trí, phân biệt đâu là Tầng Dữ Liệu và Tầng Network API.
