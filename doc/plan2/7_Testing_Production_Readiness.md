# 7. Testing & Production Readiness (Sẵn sàng Deploy)

Code xong chưa phải là xong. Code phải chạy đúng (Test) và chạy được trên mọi máy (Docker).
Đây là sự khác biệt giữa "Code dạo" và "Code chuyên nghiệp".

---

## 7.1. Testing with `pytest` & `TestClient`

FastAPI cung cấp `TestClient` dựa trên thư viện `httpx` (hoặc `requests`), cho phép bạn gọi API của chính mình mà không cần bật server uvicorn.

**Cài đặt:**
```bash
pip install pytest httpx
```

**Ví dụ Test File (`tests/test_main.py`):**
```python
from fastapi.testclient import TestClient
from main import app # Import cái app của bạn

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_todo():
    response = client.post(
        "/todos/",
        json={"title": "Test todo", "completed": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test todo"
    assert "id" in data
```

**Chạy Test:**
```bash
pytest
# Hoặc chạy chi tiết: pytest -v
```

---

## 7.2. Override Dependency (Kỹ thuật Mocking đỉnh cao)

Khi test, bạn **KHÔNG MUỐN** ghi dữ liệu vào Database thật. Bạn muốn dùng một DB giả (SQLite in-memory) hoặc một Dict giả.
Dependency Injection của FastAPI cho phép bạn thay thế (`override`) logic xử lý.

```python
from main import app, get_db
from fastapi.testclient import TestClient

# DB giả lập
fake_db = {} 

# Hàm thay thế
async def override_get_db():
    try:
        yield fake_db
    finally:
        pass

# Báo cho app biết: Khi nào gặp get_db, hãy dùng override_get_db
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user_with_fake_db():
    # Gọi API như thường, nhưng bên dưới nó đang dùng fake_db
    response = client.post("/users/", json={"email": "test@test.com"})
    assert response.status_code == 200
    assert "test@test.com" in fake_db # Kiểm tra trực tiếp vào giả lập
```
*Sau khi test xong, nhớ reset: `app.dependency_overrides = {}`.*

---

## 7.3. Docker & Docker Compose (Containerization)

Để đảm bảo "It works on my machine" cũng "Works on Server", chúng ta đóng gói app vào Docker.

**1. Tạo `Dockerfile`:**
```dockerfile
# Base image (Python nhẹ nhất)
FROM python:3.10-slim

# Thư mục làm việc trong container
WORKDIR /app

# Copy file requirements trước để tận dụng cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Mở cổng 8000
EXPOSE 8000

# Lệnh chạy server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**2. Tạo `docker-compose.yml` (Chạy cả App + DB Postgres):**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db/dbname

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**3. Chạy lên:**
```bash
docker-compose up --build
```
Lúc này bạn có cả 1 hệ thống Backend + Database chạy cô lập, sạch sẽ.

---

## 7.4. Deployment Checklist (Trước khi ra production)

1.  **Gunicorn**: `uvicorn` dùng để dev rất tốt, nhưng production nên dùng `gunicorn` quản lý worker process uvicorn.
    *   Lệnh: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`
2.  **HTTPS**: Luôn dùng HTTPS (có thể cấu hình qua Nginx hoặc Traefik làm Reverse Proxy).
3.  **Environment Variables**: KHÔNG BAO GIỜ để lộ `SECRET_KEY` hay Pass DB trong code. Dùng file `.env` và thư viện `pydantic-settings`.

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Viết Test**:
    *   Viết ít nhất 3 test cases cho API Todo của bạn (Create success, Create fail do thiếu field, Get list).
2.  **Chạy Docker**:
    *   Cài Docker Desktop.
    *   Tạo `Dockerfile` cho dự án.
    *   Build và chạy image: `docker build -t my-fastapi .` -> `docker run -p 8000:8000 my-fastapi`.
3.  **Refactor Config**:
    *   Tách các biến cấu hình (Database URL, Secret Key) ra lớp `Settings` dùng `pydantic-settings`. Đọc từ biến môi trường.

---
**TỔNG KẾT MODULE 2:**
Chúc mừng bạn! Bạn đã hoàn thành toàn bộ lộ trình Backend FastAPI.
Từ HTTP -> Pydantic -> Database Async -> Security -> Docker.
Giờ là lúc bạn kết hợp tất cả lại để xây dựng một **Sản phẩm thực tế (Real-world Project)**. Con đường chuyên nghiệp đang ở ngay trước mắt!
