# GIAI ĐOẠN 3: BLOG FEATURE (CORE FUNCTIONALITY)

Sau khi hoàn thành Phase 1 (Database) và Phase 2 (Authentication), đây là giai đoạn xây dựng tính năng chính của Blog: **Quản lý bài viết (Posts)**.

Giai đoạn này áp dụng các kiến thức từ `MASTER_PLAN.md`:
- **FastAPI Fundamentals**: Path/Query Params, Pydantic, Dependency Injection
- **Database Integration**: Async SQLAlchemy CRUD
- **Authentication**: Chỉ user đã login mới được tạo/sửa/xóa bài
- **Best Practices**: Clean Code, Type Hints, Repository Pattern

---

## 1. Cấu trúc Module Posts

Chúng ta sẽ xây dựng module `posts` hoàn chỉnh với cấu trúc tương tự module `users`:

```
app/modules/posts/
├── __init__.py
├── models.py       # ✅ Đã có sẵn từ Phase 1
├── schemas.py      # Pydantic: PostCreate, PostUpdate, PostResponse
├── crud.py         # Logic DB: create, get, update, delete
├── router.py       # API Endpoints
└── dependencies.py # (Optional) Post-specific dependencies
```

---

## 2. Pydantic Schemas (`app/modules/posts/schemas.py`)

### 2.1. Các Schema cần tạo

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema cho việc TẠO bài viết mới
class PostCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200, example="Hướng dẫn FastAPI cơ bản")
    slug: str = Field(..., pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$', example="huong-dan-fastapi-co-ban")
    content: str = Field(..., min_length=10, example="Nội dung bài viết chi tiết...")
    is_published: bool = False

# Schema cho việc CẬP NHẬT bài viết (Tất cả field đều optional)
class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    slug: Optional[str] = Field(None, pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    content: Optional[str] = Field(None, min_length=10)
    is_published: Optional[bool] = None

# Schema cho RESPONSE trả về client
class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    author_id: int
    # author_username: Optional[str] = None  # Sẽ join khi cần

    class Config:
        from_attributes = True

# Schema cho danh sách bài viết (Trang chủ)
class PostListItem(BaseModel):
    id: int
    title: str
    slug: str
    is_published: bool
    created_at: datetime
    author_id: int

    class Config:
        from_attributes = True
```

### 2.2. Giải thích các Field Validation
- `Field(..., min_length=5)`: Bắt buộc, tối thiểu 5 ký tự
- `pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$'`: Regex cho slug (chỉ chữ thường, số, gạch ngang)
- `Optional[str] = None`: Field không bắt buộc (dùng cho Update)

---

## 3. CRUD Operations (`app/modules/posts/crud.py`)

### 3.1. Các hàm CRUD cần thiết

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
from .models import Post
from .schemas import PostCreate, PostUpdate

# ========== CREATE ==========
async def create_post(db: AsyncSession, post_data: PostCreate, author_id: int) -> Post:
    """Tạo bài viết mới, gắn author_id từ user đang login"""
    db_post = Post(
        title=post_data.title,
        slug=post_data.slug,
        content=post_data.content,
        is_published=post_data.is_published,
        author_id=author_id
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

# ========== READ (Single) ==========
async def get_post_by_id(db: AsyncSession, post_id: int) -> Optional[Post]:
    """Lấy bài viết theo ID"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalars().first()

async def get_post_by_slug(db: AsyncSession, slug: str) -> Optional[Post]:
    """Lấy bài viết theo slug (URL thân thiện)"""
    result = await db.execute(select(Post).where(Post.slug == slug))
    return result.scalars().first()

# ========== READ (List with Pagination) ==========
async def get_posts(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 10,
    published_only: bool = True
) -> List[Post]:
    """
    Lấy danh sách bài viết với phân trang.
    - skip: Bỏ qua bao nhiêu bài (offset)
    - limit: Lấy tối đa bao nhiêu bài
    - published_only: Chỉ lấy bài đã publish
    """
    query = select(Post).order_by(Post.created_at.desc())
    
    if published_only:
        query = query.where(Post.is_published == True)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_posts_by_author(db: AsyncSession, author_id: int) -> List[Post]:
    """Lấy tất cả bài viết của một tác giả"""
    result = await db.execute(
        select(Post)
        .where(Post.author_id == author_id)
        .order_by(Post.created_at.desc())
    )
    return result.scalars().all()

async def count_posts(db: AsyncSession, published_only: bool = True) -> int:
    """Đếm tổng số bài viết (dùng cho pagination metadata)"""
    query = select(func.count(Post.id))
    if published_only:
        query = query.where(Post.is_published == True)
    result = await db.execute(query)
    return result.scalar()

# ========== UPDATE ==========
async def update_post(
    db: AsyncSession, 
    post_id: int, 
    post_data: PostUpdate
) -> Optional[Post]:
    """
    Cập nhật bài viết.
    Chỉ update các field được gửi lên (không None)
    """
    db_post = await get_post_by_id(db, post_id)
    if not db_post:
        return None
    
    # Chỉ update các field có giá trị
    update_data = post_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    
    await db.commit()
    await db.refresh(db_post)
    return db_post

# ========== DELETE ==========
async def delete_post(db: AsyncSession, post_id: int) -> bool:
    """Xóa bài viết. Trả về True nếu xóa thành công."""
    db_post = await get_post_by_id(db, post_id)
    if not db_post:
        return False
    
    await db.delete(db_post)
    await db.commit()
    return True
```

---

## 4. API Router (`app/modules/posts/router.py`)

### 4.1. Dependencies cần thiết

Trước khi viết router, ta cần tạo dependency để lấy **Current User** từ JWT Token:

**File: `app/core/dependencies.py`** (Thêm vào)

```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core import security
from app.modules.users import crud as user_crud
from app.modules.users.models import User

# Đã có từ trước
DbSession = Annotated[AsyncSession, Depends(get_db)]

# OAuth2 scheme để lấy token từ Header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency để lấy user hiện tại từ JWT Token.
    Raise 401 nếu token không hợp lệ.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Type Alias cho Current User (Giống DbSession)
CurrentUser = Annotated[User, Depends(get_current_user)]
```

### 4.2. Posts Router

**File: `app/modules/posts/router.py`**

```python
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from app.core.dependencies import DbSession, CurrentUser
from . import crud, schemas

router = APIRouter(prefix="/posts", tags=["Posts"])

# ========== PUBLIC ENDPOINTS ==========

@router.get("/", response_model=List[schemas.PostListItem])
async def list_posts(
    db: DbSession,
    skip: int = Query(0, ge=0, description="Số bài bỏ qua"),
    limit: int = Query(10, ge=1, le=100, description="Số bài lấy tối đa")
):
    """
    Lấy danh sách bài viết đã publish.
    Hỗ trợ phân trang với skip/limit.
    """
    posts = await crud.get_posts(db, skip=skip, limit=limit, published_only=True)
    return posts

@router.get("/{slug}", response_model=schemas.PostResponse)
async def get_post_by_slug(db: DbSession, slug: str):
    """Lấy chi tiết bài viết theo slug (URL thân thiện)"""
    post = await crud.get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

# ========== PROTECTED ENDPOINTS (Cần đăng nhập) ==========

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    db: DbSession,
    current_user: CurrentUser,
    post_data: schemas.PostCreate
):
    """
    Tạo bài viết mới.
    Yêu cầu: Phải đăng nhập (Bearer Token).
    """
    # Kiểm tra slug đã tồn tại chưa
    existing = await crud.get_post_by_slug(db, post_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    
    post = await crud.create_post(db, post_data, author_id=current_user.id)
    return post

@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(
    db: DbSession,
    current_user: CurrentUser,
    post_id: int,
    post_data: schemas.PostUpdate
):
    """
    Cập nhật bài viết.
    Yêu cầu: Phải đăng nhập và là tác giả của bài viết.
    """
    # Kiểm tra bài viết tồn tại
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Kiểm tra quyền sở hữu
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this post"
        )
    
    # Nếu đổi slug, kiểm tra trùng
    if post_data.slug and post_data.slug != post.slug:
        existing = await crud.get_post_by_slug(db, post_data.slug)
        if existing:
            raise HTTPException(status_code=400, detail="Slug already exists")
    
    updated = await crud.update_post(db, post_id, post_data)
    return updated

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    db: DbSession,
    current_user: CurrentUser,
    post_id: int
):
    """
    Xóa bài viết.
    Yêu cầu: Phải đăng nhập và là tác giả của bài viết.
    """
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    await crud.delete_post(db, post_id)
    return None  # 204 No Content

# ========== USER'S OWN POSTS ==========

@router.get("/me/posts", response_model=List[schemas.PostListItem])
async def get_my_posts(db: DbSession, current_user: CurrentUser):
    """Lấy tất cả bài viết của user hiện tại (bao gồm cả nháp)"""
    posts = await crud.get_posts_by_author(db, author_id=current_user.id)
    return posts
```

---

## 5. Đăng ký Router vào Main App

**File: `app/main.py`** (Cập nhật)

```python
from fastapi import FastAPI
from app.modules.users.router import router as user_router
from app.modules.auth.router import router as auth_router
from app.modules.posts.router import router as posts_router  # THÊM

app = FastAPI(title="Professional Blog API")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)  # THÊM

@app.get("/")
def root():
    return {"message": "Hello World from Enterprise Structure"}
```

---

## 6. Kiểm thử API (Testing Checklist)

### Sử dụng Swagger UI (`/docs`)

1. **Đăng ký user**: `POST /users/`
2. **Đăng nhập**: `POST /token` -> Copy `access_token`
3. **Authorize**: Click nút "Authorize" trên Swagger, dán token
4. **Tạo bài viết**: `POST /posts/`
5. **Xem danh sách**: `GET /posts/`
6. **Xem chi tiết theo slug**: `GET /posts/{slug}`
7. **Cập nhật bài**: `PUT /posts/{id}`
8. **Xóa bài**: `DELETE /posts/{id}`

### Các test case quan trọng
- [ ] Tạo post khi chưa login -> Expect 401
- [ ] Tạo post với slug trùng -> Expect 400
- [ ] Sửa post của người khác -> Expect 403
- [ ] Xóa post của người khác -> Expect 403
- [ ] Lấy post không tồn tại -> Expect 404

---

## 7. ACTION ITEMS (Việc cần làm)

1. [ ] Tạo file `app/modules/posts/schemas.py`
2. [ ] Tạo file `app/modules/posts/crud.py`
3. [ ] Cập nhật `app/core/dependencies.py` (thêm `get_current_user`, `CurrentUser`)
4. [ ] Tạo file `app/modules/posts/router.py`
5. [ ] Cập nhật `app/main.py` (thêm posts router)
6. [ ] Tạo file `app/modules/posts/__init__.py` (empty)
7. [ ] Test toàn bộ API qua Swagger UI

---

## 8. Kiến thức áp dụng từ MASTER_PLAN

| Mục trong Master Plan | Áp dụng trong Phase 3 |
|----------------------|----------------------|
| **Type Hinting** | Pydantic schemas với đầy đủ type |
| **Dependency Injection** | `DbSession`, `CurrentUser` |
| **Async/Await** | Tất cả CRUD operations |
| **Authentication (JWT)** | `get_current_user` dependency |
| **ORM (SQLAlchemy)** | Model `Post`, async queries |
| **Clean Code** | Tách riêng schemas, crud, router |
| **Repository Pattern** | File `crud.py` đóng vai trò Repository |

---

**Sau khi hoàn thành Phase 3**, bạn đã có một Blog API hoàn chỉnh với:
- Hệ thống User (đăng ký, đăng nhập)
- Quản lý bài viết (CRUD)
- Phân quyền (chỉ tác giả mới sửa/xóa bài của mình)
- Phân trang (pagination)

**Phase 4 (Nâng cao)** sẽ bao gồm: Comments, Categories, Search, Caching với Redis...
