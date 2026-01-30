# GIAI ĐOẠN 1: KHỞI TẠO & DATABASE (Setup & Database Foundation) - PHIÊN BẢN HOÀN CHỈNH

Văn bản này tổng hợp tất cả các kỹ thuật "xương máu" để cấu hình FastAPI + Alembic hoạt động trơn tru với PostgreSQL Schema riêng biệt (`blog_db`), tránh xóa nhầm dữ liệu ở public schema.

---

## 1. Chuẩn bị Môi trường (Environment Setup)

### Bước 1.1: Setup Virtual Environment
```powershell
python -m venv .venv
```

### Bước 1.2: Kích hoạt môi trường ảo
```powershell
# Windows PowerShell
.\.venv\Scripts\activate

# Nếu bạn dùng CMD thay vì PowerShell:
.venv\Scripts\activate.bat
```
*Dấu hiệu thành công:* Đầu dòng lệnh sẽ hiện `(.venv) C:\...`

### Bước 1.3: Tạo file `requirements.txt`
Có 2 cách:

**Cách 1 (Dùng lệnh echo - Nhanh):**
```powershell
@"
fastapi
uvicorn[standard]
sqlalchemy
alembic
asyncpg
psycopg2-binary
python-dotenv
passlib[bcrypt]
python-jose[cryptography]
python-multipart
"@ | Out-File -Encoding utf8 requirements.txt
```

**Cách 2 (Tạo thủ công):**
Tạo file `requirements.txt` bằng tay và copy nội dung sau vào:
```text
fastapi
uvicorn[standard]
sqlalchemy
alembic
asyncpg
psycopg2-binary
python-dotenv
passlib[bcrypt]
python-jose[cryptography]
python-multipart
```

### Bước 1.4: Cài đặt toàn bộ thư viện
```powershell
pip install -r requirements.txt
```

### Bước 1.5 (Tùy chọn): Xuất lại file requirements với version cụ thể
Sau khi cài xong, bạn có thể "đóng băng" các version để sau này cài lại không bị lỗi:
```powershell
pip freeze > requirements.txt
```

### Kiểm tra cài đặt thành công
```powershell
# Kiểm tra FastAPI đã cài chưa
pip show fastapi

# Hoặc kiểm tra danh sách tất cả thư viện
pip list
```

---

## 2. Cấu trúc Dự án & File Cấu hình

### 2.1. File `.env` (Lưu ý ký tự đặc biệt)
Nếu mật khẩu chứa ký tự đặc biệt (ví dụ `@`), phải encode thành `%40`.
Nếu database nằm trong schema riêng (ví dụ `learn`), URL vẫn trỏ đến DB chính.

```env
# Ví dụ: user=learn, pass=123456a@ (encode thành 123456a%40), db=learn
DATABASE_URL=postgresql+asyncpg://learn:123456a%40@localhost:5432/learn
```

### 2.2. File `database.py` (Cấu hình Schema)
Cần chỉ định `search_path` để trỏ vào schema `blog_db` thay vì `public`.

```python
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "blog_db"} # Bắt buộc

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Quan hệ: Map sang Post.author_id
    posts = relationship("Post", back_populates="author", foreign_keys="Post.author_id")

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "blog_db"} # Bắt buộc

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # KHÔNG DÙNG: author_id = Column(Integer, ForeignKey("blog_db.users.id"))
    # THAY BẰNG:
    author_id = Column(Integer, index=True) 
    
    author = relationship("User", back_populates="posts", foreign_keys=[author_id])
```

### 2.2. File `.env` (Xử lý Password đặc biệt)
Nếu pass có ký tự `@`, phải encode thành `%40`.
```env
DATABASE_URL=postgresql+asyncpg://learn:123456a%40@localhost:5432/learn
```

### 2.3. File `database.py`
```python
# ... imports ...
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    # Trỏ mặc định vào schema blog_db khi query
    connect_args={"server_settings": {"search_path": "blog_db"}}
)
# ...
```

---

## 3. Cấu hình Alembic Siêu Chuẩn (Tránh xóa nhầm DB)

### B1. File `alembic.ini`
Nhớ double ký tự `%` thành `%%` nếu có trong password.
```ini
sqlalchemy.url = postgresql://learn:123456a%%40@localhost:5432/learn
```

### B2. File `alembic/env.py` (Cấu hình bảo vệ public schema)
Đây là đoạn code quan trọng nhất để Alembic chỉ chạm vào `blog_db` và lờ đi `public`.

```python
# 1. Import Models
from models import Base
target_metadata = Base.metadata

# 2. Định nghĩa hàm lọc (Đặt ngay dưới import)
def include_object(object, name, type_, reflected, compare_to):
    # Chỉ xử lý bảng thuộc schema blog_db
    if type_ == "table" and object.schema != "blog_db":
        return False 
    return True

# ...

def run_migrations_online() -> None:
    # ...
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            
            # Cấu hình Schema
            version_table_schema="blog_db", # Bảng version cũng nằm trong blog_db
            include_schemas=True,           # Quét tất cả schema
            
            # Hàm lọc quan trọng
            include_object=include_object   
        )

        with context.begin_transaction():
            context.run_migrations()
```

---

## 4. Chạy Migration

Sau khi cấu hình chuẩn như trên:
1.  **Tạo migration**:
    ```powershell
    alembic revision --autogenerate -m "Init tables fresh"
    ```
    *Check:* File sinh ra chỉ có lệnh `create_table` cho `blog_db.users` và `blog_db.posts`. Không có lệnh `DROP TABLE`.

2.  **Apply vào DB**:
    ```powershell
    alembic upgrade head
    ```

---
**Kết quả**: Bạn có một hệ thống Migration an toàn, chạy đúng schema `blog_db`, không xung đột với các bảng cũ ở `public`, và code Model pythonic không phụ thuộc FK cứng. 🎉
