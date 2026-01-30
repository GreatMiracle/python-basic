# GIAI ĐOẠN 2: HỆ THỐNG NGƯỜI DÙNG & BẢO MẬT (ENTERPRISE STRUCTURE)

Chúng ta sẽ áp dụng cấu trúc **Modular (Domain-Driven)** ngay từ đầu. Mỗi tính năng (Feature) sẽ là một folder độc lập, chứa đầy đủ models, schemas, crud, và router của riêng nó. Đây là cấu trúc tiêu chuẩn cho các dự án lớn, dễ mở rộng và bảo trì.

---

## 1. Cấu trúc Thư mục Mới (Modular Structure)

Chúng ta sẽ tái cấu trúc dự án như sau:

```
fastapi_blog/
├── app/                        # Tất cả code nằm trong app/
│   ├── __init__.py
│   ├── main.py                 # Entry point mới
│   ├── core/                   # Các thành phần lõi dùng chung
│   │   ├── __init__.py
│   │   ├── config.py           # Load biến môi trường (Pydantic Settings)
│   │   ├── database.py         # Kết nối DB
│   │   └── security.py         # Tiện ích Hash pass & JWT
│   │
│   ├── modules/                # Chia module theo tính năng (Domain)
│   │   ├── __init__.py
│   │   ├── auth/               # Module Xác thực
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py      # Schema riêng cho login (Token)
│   │   │   └── router.py       # API /login
│   │   │
│   │   ├── users/              # Module Người dùng
│   │   │   ├── __init__.py
│   │   │   ├── models.py       # Model User
│   │   │   ├── schemas.py      # Schema UserCreate, UserResponse
│   │   │   ├── crud.py         # Logic tạo/lấy User
│   │   │   └── router.py       # API /users/
│   │   │
│   │   └── posts/              # Module Bài viết (Sẽ làm ở Phase 3)
│   │       ├── models.py
│   │       └── ...
│   │
│   └── Base.py                 # (Optional) Nơi gom tất cả Model để Alembic import
│
├── alembic/
├── .env
└── requirements.txt
```

---

## 2. Refactor Core (`app/core/`)

### 2.1. Di chuyển `database.py` vào `app/core/database.py`
Nội dung giữ nguyên, chỉ sửa đường dẫn import nếu cần.

### 2.2. Tạo `app/core/security.py`
Code xử lý Hash và JWT (tách biệt khỏi logic nghiệp vụ).

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key_tam_thoi")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

## 3. Module Users (`app/modules/users/`)

Tất cả những gì liên quan đến User bỏ vào đây.

### 3.1. `models.py` (User Model)
*Di chuyển class `User` từ file models cũ vào đây.*
```python
# app/modules/users/models.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base # Import từ core

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "blog_db"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Quan hệ với Post (String reference để tránh circular import)
    posts = relationship("app.modules.posts.models.Post", back_populates="author", foreign_keys="Post.author_id")
```

### 3.2. `schemas.py` (User Schemas)
```python
# app/modules/users/schemas.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True
```

### 3.3. `crud.py` (User Logic)
```python
# app/modules/users/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import get_password_hash
from .models import User
from .schemas import UserCreate

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()
```

### 3.4. `router.py` (User API)
```python
# app/modules/users/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from . import crud, schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse)
async def create_user_api(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(db, user)
```

---

## 4. Module Auth (`app/modules/auth/`)

Chứa logic Login và Token.

### 4.1. `schemas.py`
```python
from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str
```

### 4.2. `router.py` (Login API)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core import security
from app.modules.users import crud as user_crud 
from . import schemas

router = APIRouter(tags=["Authentication"])

@router.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_username(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## 5. Main Entry Point (`app/main.py`)

Tập hợp tất cả các router lại.

```python
from fastapi import FastAPI
from app.modules.users.router import router as user_router
from app.modules.auth.router import router as auth_router

app = FastAPI(title="Professional Blog API")

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Hello World from Enterprise Structure"}
```

---
**LƯU Ý QUAN TRỌNG KHI REFACTOR:**
1.  **Alembic**: Do file `models.py` gốc đã bị di chuyển, bạn cần sửa `alembic/env.py` để import `Base` từ đúng chỗ (hoặc tạo file `app/base.py` import tất cả model vào đó rồi import vào env.py).
2.  **Import Path**: Chạy ứng dụng từ thư mục `fastapi_blog` bằng lệnh:
    `uvicorn app.main:app --reload`
