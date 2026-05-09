# User Context — Thiết Kế Chi Tiết

**Service:** `user_service` | **Port:** 8001 | **Database:** `user_db`

---

## 1. Mô Tả Bounded Context

User Context chịu trách nhiệm toàn bộ logic **định danh, xác thực và phân quyền** cho mọi đối tượng trong hệ thống (Guest, Customer, Staff, Admin). Đây là context thượng nguồn (Upstream) — mọi service khác phụ thuộc vào token JWT do context này phát hành để kiểm tra quyền truy cập.

Việc gộp Customer Profile và Staff vào cùng User Context (thay vì tách thành 3 service riêng) bảo toàn tính gắn kết (High Cohesion): mọi logic liên quan đến **"ai là người dùng này và họ được làm gì"** đều nằm trong một ranh giới duy nhất.

**Bảo mật:** JWT (stateless auth) + Bcrypt (password hashing)

---

## 2. Actors & Use Cases

### Actors:
- **Guest** — Người dùng chưa đăng nhập
- **Customer** — Khách hàng đã đăng nhập
- **Staff** — Nhân viên (do Admin phân công)
- **Admin** — Quản trị viên hệ thống

### Use Case Tổng Quan:

```
[User Context]
    │
    ├── UC01: Đăng ký tài khoản ──────────── Guest
    ├── UC02: Đăng nhập ───────────────────── Guest
    ├── UC03: Đổi mật khẩu ────────────────── Customer, Staff, Admin
    ├── UC04: Xem Profile cá nhân ──────────── Customer
    ├── UC05: Cập nhật Profile ─────────────── Customer
    ├── UC06: Quản lý địa chỉ giao hàng ───── Customer
    ├── UC07: Xem hạng thành viên ──────────── Customer
    ├── UC08: Xem danh sách nhân viên ──────── Admin
    ├── UC09: Tạo / Cập nhật tài khoản Staff── Admin
    ├── UC10: Phân quyền Staff ─────────────── Admin
    ├── UC11: Xem thông tin cá nhân (Staff) ── Staff
    └── UC12: Đăng xuất / Thu hồi token ───── Customer, Staff, Admin
```

### Mô tả Use Case Chi Tiết:

| UC | Tên | Actor | Mô tả ngắn |
|---|---|---|---|
| UC01 | Đăng ký | Guest | Tạo tài khoản Customer với email + password (Bcrypt hash) |
| UC02 | Đăng nhập | Guest | Xác thực credentials → trả về JWT access + refresh token |
| UC03 | Đổi mật khẩu | Customer/Staff/Admin | Nhập mật khẩu cũ, xác nhận mật khẩu mới (Bcrypt re-hash) |
| UC04 | Xem Profile | Customer | Xem thông tin cá nhân, điểm tích lũy, hạng thành viên |
| UC05 | Cập nhật Profile | Customer | Sửa tên, ngày sinh, avatar, số điện thoại |
| UC06 | Quản lý Address | Customer | Thêm/sửa/xóa địa chỉ giao hàng, đặt địa chỉ mặc định |
| UC07 | Xem hạng | Customer | Xem membership tier hiện tại và điều kiện lên hạng |
| UC08 | Danh sách Staff | Admin | Xem danh sách nhân viên, lọc theo phòng ban |
| UC09 | Tạo Staff | Admin | Tạo tài khoản nhân viên, gán phòng ban |
| UC10 | Phân quyền | Admin | Gán role cho Staff (warehouse/customer_support/...) |
| UC11 | Xem profile Staff | Staff | Xem thông tin cá nhân của bản thân |
| UC12 | Đăng xuất | Customer/Staff/Admin | Blacklist refresh token (invalidate session) |

---

## 3. Entities & Attributes

### 3.1 `User` — Aggregate Root
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| username | string (unique, indexed) | Dùng cho Staff login |
| email | string (unique, indexed) | Dùng cho Customer login |
| password | string | Bcrypt hash, KHÔNG lưu plain-text |
| user_type | enum | `customer` / `staff` / `admin` |
| role | string | Role chi tiết của Staff (warehouse, support...) |
| name | string | Tên hiển thị |
| is_active | boolean | Soft-delete: False = tài khoản bị khóa |
| date_joined | datetime | |
| last_login | datetime | |

### 3.2 `CustomerProfile` — Entity (thuộc User Aggregate)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| user_id | int | FK nội bộ → User |
| phone | string | |
| date_of_birth | datetime | |
| avatar_url | string | |
| points | int | Điểm tích lũy (loyalty points) |
| membership_tier | string | Bronze / Silver / Gold / Platinum |
| created_at | datetime | |

### 3.3 `Address` — Value Object (thuộc CustomerProfile)
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| customer_profile_id | int | FK nội bộ → CustomerProfile |
| street | string | |
| city | string | |
| state | string | |
| zip_code | string | |
| country | string | Mặc định "Vietnam" |
| is_default | boolean | Địa chỉ giao hàng mặc định |

### 3.4 `StaffMember` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| user_id | int | FK nội bộ → User (unique) |
| department_id | int | FK nội bộ → StaffDepartment |
| phone | string | |
| hire_date | datetime | |
| salary | int | |
| is_active | boolean | |

### 3.5 `StaffDepartment` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| name | string (unique) | Warehouse, Customer Support, ... |
| description | text | |

### 3.6 `MembershipTier` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| name | string (unique) | Bronze / Silver / Gold / Platinum |
| min_points | int | Ngưỡng điểm tối thiểu để đạt hạng |
| discount_percent | float | % giảm giá cho hạng này |
| free_shipping | boolean | Miễn phí vận chuyển không |

### 3.7 `ReferralCode` — Entity
| Thuộc tính | Kiểu | Ghi chú |
|---|---|---|
| id | int (PK) | |
| code | string (unique) | |
| owner_customer_id | int | Soft ref → User (customer) |
| reward_points | int | Điểm thưởng khi bạn đăng ký dùng mã |
| is_active | boolean | |
| used_count | int | |

---

## 4. Relationships

| Quan hệ | Từ | Đến | Lực hút | Cardinality |
|---|---|---|---|---|
| Composition | User | CustomerProfile | Has-parts (vòng đời phụ thuộc) | 1..1 → 0..1 |
| Composition | CustomerProfile | Address | Has-parts (cascade delete) | 1..1 → 0..* |
| Composition | User | StaffMember | Has-parts | 1..1 → 0..1 |
| Association | StaffMember | StaffDepartment | Belongs-to | 0..* → 1..1 |
| Association | CustomerProfile | MembershipTier | References | 0..* → 1..1 |
| Association | User | ReferralCode | Owns | 1..1 → 0..1 |

**Quan hệ Xuyên Domain (Soft Reference):**
- `Cart.customer_id` → User.id *(chỉ lưu ID)*
- `Order.customer_id` → User.id *(chỉ lưu ID)*
- `Payment.customer_id` → User.id *(chỉ lưu ID)*

---

## 5. Luồng Hoạt Động Cơ Bản

### Flow UC01: Đăng ký Customer
```
Guest → POST /users/register
  1. Validate email unique
  2. Bcrypt hash password
  3. Tạo User (user_type='customer')
  4. Tạo CustomerProfile (points=0, tier='Bronze')
  5. Trả về user info (không trả về token)
```

### Flow UC02: Đăng nhập
```
Guest → POST /users/login
  1. Tìm User theo email (customer) hoặc username (staff/admin)
  2. Bcrypt verify password
  3. Tạo JWT access token (exp: 1h) + refresh token (exp: 7d)
  4. Lưu refresh token (để blacklist khi logout)
  5. Trả về {access_token, refresh_token, user_type, role}
```

### Flow UC06: Quản lý Address
```
Customer → POST /users/me/addresses
  1. Verify JWT (customer role)
  2. Tạo Address gắn vào CustomerProfile
  3. Nếu is_default=True: reset toàn bộ địa chỉ cũ về False trước

Customer → DELETE /users/me/addresses/{id}
  1. Verify JWT + ownership
  2. Cascade delete Address
  3. Nếu xóa địa chỉ default: set địa chỉ đầu tiên còn lại làm default
```

---

## 6. API Endpoints Chính

| Method | Endpoint | Actor | Mô tả |
|---|---|---|---|
| POST | `/users/register` | Guest | Đăng ký |
| POST | `/users/login` | Guest | Đăng nhập → JWT |
| POST | `/users/logout` | Auth | Blacklist token |
| POST | `/users/token/refresh` | Auth | Refresh JWT |
| GET | `/users/me` | Customer | Xem profile |
| PATCH | `/users/me` | Customer | Cập nhật profile |
| GET | `/users/me/addresses` | Customer | Danh sách địa chỉ |
| POST | `/users/me/addresses` | Customer | Thêm địa chỉ |
| PATCH | `/users/me/addresses/{id}` | Customer | Sửa địa chỉ |
| DELETE | `/users/me/addresses/{id}` | Customer | Xóa địa chỉ |
| GET | `/users/me/membership` | Customer | Xem hạng + điểm |
| GET | `/users/staffs` | Admin | Danh sách Staff |
| POST | `/users/staffs` | Admin | Tạo Staff |
| PATCH | `/users/staffs/{id}` | Admin | Cập nhật Staff |

---

## 7. Django Apps Nội Bộ

```
user_service/
├── users/          ← User model, auth views (login/register/logout)
├── customers/      ← CustomerProfile, Address
├── staffs/         ← StaffMember, StaffDepartment
└── membership/     ← MembershipTier, ReferralCode
```

## 8. Ghi Chú Migration

- **Rename database:** `auth_db` → `user_db`
- **Nguồn data:** `auth_service/users/`, `customer_service/customers/`, `staff_service/staffs/`
- `LoyaltyPoints` từ `interaction_service` → merge vào `CustomerProfile.points`
- `MembershipTier`, `ReferralCode` từ `marketing_service` → app `membership/`
