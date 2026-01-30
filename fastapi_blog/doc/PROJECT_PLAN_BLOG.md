# KẾ HOẠCH BÀI BẢN: XÂY DỰNG FASTAPI BLOG (PostgreSQL)

Chào bạn, đây là bản thiết kế chi tiết (Blue-print) để xây dựng một **Blog API chuẩn Production** sử dụng FastAPI và PostgreSQL. Chúng ta sẽ không code "đại" mà đi theo một cấu trúc MVC hiện đại, dễ mở rộng.

---

## 1. Công nghệ sử dụng (Tech Stack)
*   **Ngôn ngữ**: Python 3.10+
*   **Web Framework**: FastAPI (High performance).
*   **Database**: PostgreSQL (Relational DB chuẩn mực).
*   **ORM**: SQLAlchemy 2.0 (Async) - Tương tác DB bằng Python Class.
*   **Migration**: Alembic - Quản lý lịch sử thay đổi DB.
*   **Docker**: Để chạy PostgreSQL mà không cần cài rác máy.

---

## 2. Thiết kế Database (ERD Design)

Chúng ta sẽ có 3 bảng (Entities) cốt lõi cho một Blog đơn giản:

### Bảng 1: `users` (Người dùng)
Lưu thông tin tác giả/người đọc.
*   `id`: Integer (Primary Key, Auto-increment).
*   `username`: String (Unique, Index).
*   `email`: String (Unique, Index).
*   `hashed_password`: String (Mật khẩu đã mã hóa).
*   `is_active`: Boolean (Để block user nếu cần).
*   `role`: String (Ví dụ: "admin", "writer", "reader").

### Bảng 2: `posts` (Bài viết)
Nội dung chính của Blog.
*   `id`: Integer (Primary Key).
*   `title`: String (Tiêu đề bài viết).
*   `slug`: String (URL thân thiện, VD: `hoc-fastapi-co-ban`, Unique).
*   `content`: Text (Nội dung dài).
*   `is_published`: Boolean (Nháp hay đã đăng).
*   `created_at`: DateTime (Ngày tạo).
*   `updated_at`: DateTime (Ngày sửa cuối).
*   `author_id`: Integer (Foreign Key -> `users.id`). **Quan hệ 1-N**: Một user viết nhiều bài.

### Bảng 3: `comments` (Bình luận - Optional cho Phase 2)
*   `id`: Integer.
*   `content`: Text.
*   `post_id`: Integer (Foreign Key -> `posts.id`).
*   `author_id`: Integer (Foreign Key -> `users.id`).

---

## 3. Cấu trúc thư mục (Project Structure)

Chúng ta sẽ dùng cấu trúc gom theo feature (module) hoặc theo layer. Với blog nhỏ, gom theo layer (Controller-Service-Repository) là dễ hiểu nhất.

```
fastapi_blog/
├── .env                   # Chứa pass DB, Secret Key (Ko up lên git)
├── main.py                # Entry point, chạy App
├── database.py            # Cấu hình kết nối DB (Async Engine)
├── models.py              # Định nghĩa bảng (SqlAlchemy Classes)
├── schemas.py             # Pydantic Models (Input/Output validation)
├── crud.py                # Logic tương tác DB (Create, Read...)
├── routers/               # Chia nhỏ API
│   ├── users.py           # API liên quan user (Login, Register)
│   └── posts.py           # API liên quan bài viết
└── alembic/               # Thư mục Migration tự sinh
```

---

## 4. Lộ trình thực hiện (Implementation Steps)

### Giai đoạn 1: Khởi tạo & Database
1.  **Môi trường**: Tạo `venv`, cài `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `asyncpg`, `psycopg2-binary`.
2.  **Docker PostgreSQL**: Tạo file `docker-compose.yml` để bật DB Postgres chỉ với 1 lệnh.
3.  **Models**: Viết code trong `models.py` định nghĩa bảng User và Post.
4.  **Migration**: Chạy `alembic init`, `alembic revision --autogenerate`, `alembic upgrade head` để tạo bảng thật trong DB.

### Giai đoạn 2: User System (Authentication)
1.  **Schemas**: Tạo Pydantic model `UserCreate`, `UserResponse`.
2.  **CRUD**: Viết hàm `create_user` (nhớ hash password), `Get User`.
3.  **API**: Viết file `routers/users.py` với endpoint `/register`.
4.  **Login**: Thêm endpoint `/login` trả về JWT Token (như bài 5 module 2).

### Giai đoạn 3: Blog Feature (Core)
1.  **Schemas**: Tạo `PostCreate`, `PostUpdate`, `PostResponse`.
2.  **CRUD**:
    *   `create_post`: Chỉ user đã login mới được tạo.
    *   `get_posts`: Lấy danh sách (có phân trang skip/limit).
    *   `delete_post`: Chỉ tác giả mới được xóa bài của mình.
3.  **API**: Viết `routers/posts.py`.

---

## 5. File `docker-compose.yml` (Tặng kèm để chạy DB ngay)

Bạn hãy tạo file `docker-compose.yml` ở thư mục gốc:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: blog_postgres
    restart: always
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=password123
      - POSTGRES_DB=blog_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Sau đó chạy lệnh: `docker-compose up -d`. Thế là có ngay 1 con server PostgreSQL đang chạy ở port 5432!

---
Bạn có muốn tôi bắt đầu hướng dẫn code chi tiết **Giai đoạn 1 (Setup Models & Database)** cho dự án này không?
