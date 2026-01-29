# KẾ HOẠCH CHI TIẾT: BACKEND DEVELOPMENT & FASTAPI MASTERY

File này chi tiết hóa phần **"2. Backend Development & FastAPI"** từ [MASTER_PLAN.md](./MASTER_PLAN.md). Đây là giai đoạn chuyển bạn từ "người biết ngôn ngữ" thành "người làm sản phẩm".

---

## 1. Nền tảng HTTP & Thiết kế API (HTTP & API Design Foundations)
*Code giỏi mà không hiểu giao thức mạng thì cũng như xây nhà trên cát. Phải nắm vững cách Web hoạt động.*

*   [ ] **Giao thức HTTP**:
    *   Request/Response Cycle.
    *   HTTP Methods: `GET` (đọc), `POST` (tạo), `PUT` (sửa hết), `PATCH` (sửa 1 phần), `DELETE` (xóa).
    *   Status Codes: `2xx` (Success), `3xx` (Redirect), `4xx` (Client Error), `5xx` (Server Error).
    *   Headers: `Content-Type`, `Authorization`, `User-Agent`.
*   [ ] **RESTful API Standard**:
    *   Quy tắc đặt tên Endpoint (URL Naming Convention).
    *   Statelessness (Không lưu trạng thái).
    *   Idempotency (Tính bất biến khi gọi nhiều lần).
*   [ ] **Tools**:
    *   Sử dụng **Postman** hoặc **curl** để test API.
    *   Đọc và hiểu Swagger UI (Docs tự động của FastAPI).

## 2. FastAPI Core & Routing (Cấu trúc ứng dụng)
*Bắt đầu xây dựng những endpoint đầu tiên và tổ chức code gọn gàng.*

*   [ ] **Hello World & Basic Routing**:
    *   `@app.get("/")`, `@app.post("/items")`.
    *   Path Parameters (`/items/{item_id}`) vs Query Parameters (`/items?skip=0&limit=10`).
*   [ ] **Request Body & Pydantic**:
    *   Tạo Pydantic Model cho dữ liệu đầu vào (Input Schema).
    *   Tự động validate và chuyển đổi kiểu dữ liệu.
    *   Nested Models (Model lồng nhau).
*   [ ] **Response Model**:
    *   Kiểm soát dữ liệu trả về (ẩn password, lọc field thừa).
    *   `response_model`, `response_model_exclude_unset`.
*   [ ] **Cấu trúc dự án (Project Structure)**:
    *   Tách file `main.py`.
    *   Sử dụng `APIRouter` để chia nhỏ module (`routers/users.py`, `routers/items.py`).

## 3. Dependency Injection (DI) - Trái tim của FastAPI
*Đây là tính năng mạnh nhất giúp code FastAPI clean, dễ test và tái sử dụng.*

*   [ ] **Cơ bản về Depends**:
    *   Viết hàm dependency đơn giản.
    *   Tái sử dụng logic (ví dụ: phân trang common).
*   [ ] **Advanced DI**:
    *   Dependency trả về Generator (dùng cho kết nối DB `yield session`).
    *   Class-based Dependencies.
    *   Global Dependencies (Áp dụng cho toàn bộ App hoặc Router).

## 4. Database Integration (Async SQLAlchemy & Alembic)
*Kết nối cơ sở dữ liệu theo phong cách hiện đại (Async).*

*   [ ] **Thiết lập môi trường DB**:
    *   Cài đặt PostgreSQL (hoặc MySQL) và driver async (ví dụ `asyncpg`).
    *   Cấu hình `SQLAlchemy` engine và session.
*   [ ] **ORM Models**:
    *   Định nghĩa Table bằng Python Class (Declarative Base).
    *   Quan hệ (Relationships): One-to-Many, Many-to-Many.
*   [ ] **CRUD Operations (Async)**:
    *   Viết các hàm Create, Read, Update, Delete với `await`.
    *   Xử lý lỗi `NoResultFound`, `IntegrityError`.
*   [ ] **Migrations với Alembic**:
    *   Khởi tạo Alembic.
    *   Tạo file migration (`alembic revision --autogenerate`).
    *   Chạy migration (`alembic upgrade head`).

## 5. Authentication & Security (Bảo mật)
*Bảo vệ API khỏi truy cập trái phép.*

*   [ ] **OAuth2 & JWT (JSON Web Tokens)**:
    *   Cơ chế: Login -> Nhận Token -> Gửi Token kèm Request.
    *   Tạo endpoint `/login` (OAuth2PasswordRequestForm).
*   [ ] **Password Handling**:
    *   Hashing mật khẩu với thư viện `passlib` và thuật toán `bcrypt`.
    *   Tuyệt đối không lưu plain-text password.
*   [ ] **Protecting Routes**:
    *   Viết Dependency `get_current_user` để lấy user từ Token.
    *   Chặn truy cập endpoint nếu Token không hợp lệ.
*   [ ] **CORS (Cross-Origin Resource Sharing)**:
    *   Cấu hình để Frontend (React/Vue) gọi được API.

## 6. Background Tasks & Performance
*Xử lý các tác vụ nặng mà không bắt người dùng phải chờ đợi.*

*   [ ] **Background Tasks (Built-in)**:
    *   Gửi email, ghi log, xử lý file sau khi response đã trả về.
*   [ ] **Caching với Redis**:
    *   Cài đặt Redis.
    *   Cache kết quả của các query nặng.
*   [ ] **Celery (Optional - Advanced)**:
    *   Hàng đợi tác vụ chuyên nghiệp (Task Queue) cho hệ thống lớn.

## 7. Testing & Production Readiness
*Đảm bảo code chất lượng trước khi deploy.*

*   [ ] **Testing FastAPI**:
    *   Sử dụng `TestClient` (dựa trên `httpx`).
    *   Viết test case cho các API endpoints.
    *   Override Dependency để mock database khi test.
*   [ ] **Dockerizing**:
    *   Viết `Dockerfile` tối ưu cho Python App.
    *   Dùng `docker-compose` để chạy cả App và DB cùng lúc.

---
**Hướng dẫn học**:
1.  Chúng ta sẽ đi tuần tự từ phần 1 đến phần 5 (Đây là xương sống của một Backend Dev).
2.  Phần 6 và 7 có thể học sau khi đã làm xong một dự án nhỏ (Project-based learning).
3.  **Dự án thực hành gợi ý**: Xây dựng một **Todo App** hoặc **Blog API** có đầy đủ Đăng ký, Đăng nhập, CRUD bài viết.
