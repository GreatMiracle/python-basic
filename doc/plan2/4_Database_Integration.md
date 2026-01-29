# 4. Database Integration (Async SQLAlchemy & Alembic)

Đây là phần "xương xẩu" nhất nhưng quan trọng nhất. Một Backend không có DB chỉ là cái vỏ rỗng.
Chúng ta sẽ sử dụng stack hiện đại nhất 2024: **FastAPI + Async SQLAlchemy 2.0 + PostgreSQL + Alembic**.

---

## 4.1. Cài đặt Driver và Thư viện

Chúng ta cần `sqlalchmey` (ORM) và `asyncpg` (Driver async hiệu năng cao cho Postgres).

```bash
pip install sqlalchemy asyncpg alembic
# Nếu dùng SQLite cho đơn giản lúc đầu:
pip install aiosqlite
```

---

## 4.2. Cấu hình Database (`database.py`)

Cấu trúc file `database.py` chuẩn Async:

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# URL kết nối (Ví dụ dùng SQLite cho dễ test, Production thì đổi sang Postgres)
# Lưu ý: Cần prefix 'sqlite+aiosqlite:///'
DATABASE_URL = "sqlite+aiosqlite:///./test.db" 
# Nếu là Postgres: "postgresql+asyncpg://user:pass@localhost/dbname"

# 1. Tạo Engine (Cỗ máy kết nối)
engine = create_async_engine(DATABASE_URL, echo=True) # echo=True để hiện SQL log

# 2. Tạo Session Factory (Nhà máy sản xuất Session)
SessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 3. Base Class cho Models
class Base(DeclarativeBase):
    pass

# 4. Dependency lấy DB (Dùng trong Router)
async def get_db():
    async with SessionLocal() as session:
        yield session
```

---

## 4.3. Tạo Model (ORM Models)

Tạo file `models.py`. Model là ánh xạ của bảng trong Database thành Class Python.

```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Quan hệ 1-nhiều: 1 User có nhiều Items
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

---

## 4.4. Migrations với Alembic (Quản lý thay đổi DB)

Bạn không nên tạo bảng bằng tay (SQL). Hãy dùng Alembic để versioning DB giống như Git versioning code.

**B1. Khởi tạo Alembic (Chạy 1 lần đầu):**
```bash
alembic init alembic
```

**B2. Cấu hình (`alembic/env.py`):**
Mở file `alembic/env.py`, sửa đoạn import để Alembic tìm thấy models của bạn:
```python
# Import model để Alembic biết
from models import Base 
target_metadata = Base.metadata

# Chỉnh URL kết nối trong này (hoặc trong alembic.ini)
```
*Lưu ý: Setup Alembic Async hơi phức tạp một chút về config driver, nếu mới học có thể dùng `app.on_event("startup")` để tạo bảng nhanh `await conn.run_sync(Base.metadata.create_all)`.*

**B3. Tạo migration script:**
```bash
alembic revision --autogenerate -m "Init tables"
```
Alembic sẽ quét models.py và so sánh với DB, phát hiện bạn vừa thêm bảng User và Item. Nó sinh ra file script trong `alembic/versions`.

**B4. Chạy migration (Upgrade DB):**
```bash
alembic upgrade head
```
Lúc này file `test.db` mới thực sự được tạo ra các bảng.

---

## 4.5. CRUD Operations (Async)

Viết logic trong file `crud.py`. Lưu ý cú pháp `select` và `await`.

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Item, User

# Lấy 1 User theo ID
async def get_user(db: AsyncSession, user_id: int):
    # Cú pháp mới SQLAlchemy 2.0
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# Tạo User mới
async def create_user(db: AsyncSession, email: str, pass_hash: str):
    new_user = User(email=email, hashed_password=pass_hash)
    db.add(new_user)
    await db.commit() # Lưu vào DB
    await db.refresh(new_user) # Lấy lại ID vừa tự sinh
    return new_user
```

---

## 4.6. Sử dụng trong Router

Kết hợp Dependency `get_db` và logic CRUD.

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import crud

router = APIRouter()

@router.post("/users/")
async def create_user_api(email: str, password: str, db: AsyncSession = Depends(get_db)):
    # Check trùng email...
    return await crud.create_user(db, email, password)

@router.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Setup Environment**:
    *   Tạo folder `database` trong dự án.
    *   Cài thư viện và thiết lập `database.py` dùng SQLite (cho dễ) hoặc Postgres (nếu có Docker).
2.  **Todo Models**:
    *   Tạo bảng `todos` với các cột: `id`, `title`, `description`, `completed` (boolean), `created_at` (datetime).
    *   Chạy Alembic để tạo bảng trong DB.
3.  **CRUD API**:
    *   Viết full bộ API: `Create Todo`, `Get All Todos`, `Get Todo By ID`, `Update Status`.
    *   Dùng **Postman** gọi thử API Create -> Kiểm tra file `.db` xem dữ liệu vào chưa (Dùng phần mềm **DB Browser for SQLite**).

*Lưu ý: Chuyển từ Sync sang Async với Database là bước cản lớn nhất của người mới. Hãy kiên nhẫn, khi quen rồi bạn sẽ thấy nó cực nhanh!*
