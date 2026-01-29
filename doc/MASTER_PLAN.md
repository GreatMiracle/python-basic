# MASTER PLAN: Lộ trình trở thành Senior Python Developer (Chuyên sâu Backend & FastAPI)

Chào bạn, với tư cách là một Senior Python Developer và Mentor, tôi đã thiết kế lộ trình này giúp bạn chuyển từ người học cơ bản sang một kỹ sư phần mềm chuyên nghiệp, sẵn sàng cho môi trường doanh nghiệp (Production-Ready).

Trọng tâm của lộ trình này là **Python Backend Modern** với **FastAPI** - một trong những framework mạnh mẽ và được ưa chuộng nhất hiện nay.

---

## 1. Python Core - Nền tảng vững chắc
**Mục đích:** Viết code đúng chuẩn ("Pythonic"), tối ưu và dễ bảo trì. Framework chỉ là công cụ, ngôn ngữ mới là gốc rễ.

### Kiến thức Bắt buộc (Must Know)
- [ ] **Data Structures & Algorithms**: Nắm vững `list`, `dict`, `set`, `tuple` và độ phức tạp (Big O) của các thao tác trên chúng.
- [ ] **Advanced OOP**: Magic methods (`__init__`, `__str__`, `__call__`), Inheritance, Polymorphism, Abstraction.
- [ ] **Functional Programming cơ bản**: Lambda, map, filter, decorators (rất quan trọng cho FastAPI), generators (`yield`).
- [ ] **Type Hinting**: `typing` module (`List`, `Dict`, `Optional`, `Union`). Đây là nền tảng cốt lõi của **FastAPI** và **Pydantic**.
- [ ] **Package Management**: Hiểu rõ `pip`, `venv` (virtual environment), hoặc hiện đại hơn là `poetry`.

### Kiến thức Nâng cao / Chuyên sâu
- [ ] **Metaclasses**: Hiểu cách class được tạo ra (ít dùng nhưng giúp hiểu sâu framework).
- [ ] **Concurrency & Parallelism**: Phân biệt rõ `Threading` vs `Multiprocessing`. Khi nào dùng cái nào (IO-bound vs CPU-bound).
- [ ] **Python Internals**: GIL (Global Interpreter Lock), Garbage Collection, Memory Management.

---

## 2. Backend Development & FastAPI - Trái tim của hệ thống
**Mục đích**: Xây dựng các ứng dụng web tốc độ cao, khả năng mở rộng tốt và chuẩn hóa giao tiếp dữ liệu.

### Kiến thức Bắt buộc (Must Know)
- [ ] **HTTP & RESTful API**: Methods (GET, POST, PUT, DELETE), Status Codes, Headers.
- [ ] **FastAPI Fundamentals**:
    - Path & Query Parameters.
    - **Pydantic**: Data validation & serialization (cực kỳ quan trọng).
    - **Dependency Injection**: Design pattern cốt lõi của FastAPI.
- [ ] **Asynchronous Programming (`async`/`await`)**:
    - Hiểu Event Loop.
    - Viết code non-blocking. Đây là lý do FastAPI nhanh hơn Flask/Django cũ.
- [ ] **Database Integration**:
    - **ORM**: SQLAlchemy (phiên bản 2.0 style async), Tortoise ORM.
    - **Migration**: Alembic (quản lý thay đổi cấu trúc DB).
- [ ] **Authentication & Security**:
    - OAuth2, JWT (JSON Web Tokens).
    - Hashing passwords (bcrypt/argon2).
    - CORS, SQL Injection prevention.

### Kiến thức Nâng cao / Chuyên sâu
- [ ] **Advanced FastAPI**: Websockets, Middleware custom, Background Tasks.
- [ ] **Performance Tuning**: Profiling API, Caching (Redis) để giảm tải DB.
- [ ] **Rate Limiting**: Chống spam request.
- [ ] **GraphQL**: Một giải pháp thay thế REST cho các query phức tạp (thư viện Strawberry).
- [ ] **Message Queues**: Tách các tác vụ nặng (gửi email, xử lý ảnh) ra khỏi request chính bằng Celery + Redis/RabbitMQ.

---

## 3. Database & Data Design
**Mục đích**: Lưu trữ, truy xuất dữ liệu hiệu quả và toàn vẹn.

### Kiến thức Bắt buộc (Must Know)
- [ ] **Relational DB (SQL)**: PostgreSQL (ưu tiên số 1), MySQL. Viết query JOIN, Indexing cơ bản.
- [ ] **Design Schema**: Normalization (Chuẩn hóa dữ liệu), Quan hệ 1-1, 1-n, n-n.
- [ ] **NoSQL (Cơ bản)**: Redis (dùng cho caching/session), MongoDB (document store).

### Kiến thức Nâng cao / Chuyên sâu
- [ ] **Query Optimization**: `EXPLAIN ANALYZE`, tối ưu Index phức tạp.
- [ ] **Transactions**: ACID, Isolation levels (tránh Race Conditions).
- [ ] **Replication & Sharding**: Kiến trúc DB cho hệ thống lớn.

---

## 4. Testing & Software Quality
**Mục đích**: "Code chạy được" chưa đủ, phải là "Code chạy đúng và không hỏng khi sửa đổi".

### Kiến thức Bắt buộc (Must Know)
- [ ] **Unit Testing**: `pytest` (Mạnh mẽ hơn `unittest` mặc định).
- [ ] **Fixtures & Mocking**: Giả lập DB hoặc API bên ngoài để test độc lập.
- [ ] **Integration Testing**: Test luồng hoạt động thực tế của API (gọi endpoint -> check DB).

### Kiến thức Nâng cao / Chuyên sâu
- [ ] **TDD (Test Driven Development)**: Viết test trước khi viết code.
- [ ] **Load Testing**: Dùng `Locust` hoặc `k6` để kiểm tra sức chịu tải của API.
- [ ] **Coverage**: Đảm bảo test bao phủ bao nhiêu % code.

---

## 5. DevOps & Deployment
**Mục đích**: Đưa code từ máy cá nhân lên server chạy thật (Production).

### Kiến thức Bắt buộc (Must Know)
- [ ] **Linux Basic**: Các lệnh terminal cơ bản (`ssh`, `grep`, `systemd`, `permissions`).
- [ ] **Docker**: Containerization. Viết `Dockerfile` tối ưu, `docker-compose` cho môi trường dev.
- [ ] **Web Servers**: Gunicorn (WSGI) hoặc Uvicorn (ASGI - bắt buộc cho FastAPI) + Nginx (Reverse Proxy).

### Kiến thức Nâng cao / Chuyên sâu
- [ ] **CI/CD**: GitHub Actions / GitLab CI. Tự động chạy test và deploy khi push code.
- [ ] **Cloud Providers**: AWS (EC2, S3, RDS) hoặc Google Cloud.
- [ ] **Kubernetes (K8s)**: Quản lý container ở quy mô lớn (Concept cơ bản).

---

## 6. Best Practices & Design Patterns
**Mục đích**: Code dễ đọc, dễ sửa, dễ làm việc nhóm.

- [ ] **PEP 8**: Chuẩn format code Python.
- [ ] **Linting & Formatting Tools**: Sử dụng `Ruff` (nhanh, hiện đại) hoặc `Black`, `Isort`, `Pylint`.
- [ ] **Clean Code**: Đặt tên biến, hàm rõ nghĩa. Hàm làm 1 việc duy nhất (Single Responsibility).
- [ ] **Design Patterns**: Singleton, Factory, Strategy, Repository Pattern (thường dùng để tách logic DB khỏi API).

---

## Gợi ý định hướng nghề nghiệp

1.  **Backend Developer (Python focus)**:
    *   *Tập trung*: FastAPI/Django, SQL, Redis, Docker, REST/GraphQL.
    *   *Công việc*: Xây dựng API cho Web/Mobile App, xử lý Logic nghiệp vụ.

2.  **Data Engineer**:
    *   *Tập trung*: Python, SQL nâng cao, Spark, Airflow, ETL pipelines.
    *   *Công việc*: Xây dựng luồng dữ liệu, kho dữ liệu (Data Warehouse).

3.  **AI/ML Engineer**:
    *   *Tập trung*: Python, NumPy, Pandas, PyTorch/TensorFlow, Serving API (FastAPI để deploy model).

---

## Sai lầm phổ biến cần tránh (Common Pitfalls)

1.  **Học lan man**: Cố học Django, Flask, FastAPI cùng lúc. -> **Lời khuyên**: Master FastAPI trước, tư duy backend giống nhau cả thôi.
2.  **Chặn (Blocking) Event Loop**: Dùng thư viện đồng bộ (như `requests` hay `time.sleep`) trong hàm `async def` của FastAPI. Điều này sẽ giết chết hiệu năng.
3.  **Bỏ qua Testing**: Nghĩ rằng "Test tay chạy là được". -> Hậu quả: Sửa cái này hỏng cái kia khi project lớn lên.
4.  **Lộ Secrets**: Hardcode password/API Key trong code và push lên Git. -> **Lời khuyên**: Luôn dùng biến môi trường (`.env`).
5.  **Không dùng Type Hint**: Viết Python kiểu cũ không khai báo kiểu dữ liệu. -> Hậu quả: FastAPI không validate được data, code khó debug.

---
**Lời nhắn**: Con đường này không ngắn, nhưng rất rõ ràng. Hãy bắt đầu từ **Core vững chắc**, sau đó nhảy vào **FastAPI + Database**. Thực hành bằng cách làm các project thực tế (như Todo App, E-commerce simple, Blog platform) là cách học nhanh nhất. Chúc bạn thành công!
