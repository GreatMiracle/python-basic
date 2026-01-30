# GIAI ĐOẠN 3a: CHỨC NĂNG BÌNH LUẬN (COMMENTS FEATURE)

Đây là phần mở rộng của Phase 3, thêm tính năng bình luận cho bài viết. Người dùng có thể:
- Xem bình luận của bài viết (Public)
- Thêm bình luận (Cần đăng nhập)
- Sửa/Xóa bình luận của mình

---

## 1. Thiết kế Database

### Bảng `comments`
| Column | Type | Mô tả |
|--------|------|-------|
| `id` | Integer | Primary Key |
| `content` | Text | Nội dung bình luận |
| `created_at` | DateTime | Thời gian tạo |
| `updated_at` | DateTime | Thời gian sửa |
| `post_id` | Integer | ID bài viết được comment |
| `author_id` | Integer | ID người viết comment |

---

## 2. Cấu trúc Module Comments

```
app/modules/comments/
├── __init__.py
├── models.py       # Model Comment
├── schemas.py      # Pydantic schemas
├── crud.py         # CRUD operations
└── router.py       # API endpoints
```

---

## 3. Model (`app/modules/comments/models.py`)

```python
# app/modules/comments/models.py
from sqlalchemy import Column, Integer, Text, DateTime
from app.core.database import Base
import datetime

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"schema": "blog_db"}

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Quan hệ (xử lý ở tầng CRUD)
    post_id = Column(Integer, index=True, nullable=False)
    author_id = Column(Integer, index=True, nullable=False)
```

---

## 4. Alembic Migration

Sau khi tạo model, chạy migration:

```powershell
cd fastapi_blog
alembic revision --autogenerate -m "Add comments table"
alembic upgrade head
```

---

## 5. Pydantic Schemas (`app/modules/comments/schemas.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema cho việc TẠO comment
class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, example="Bài viết rất hay!")

# Schema cho việc CẬP NHẬT comment
class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)

# Schema cho RESPONSE đơn lẻ
class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    post_id: int
    author_id: int

    class Config:
        from_attributes = True

# Schema cho comment kèm thông tin author (Optional - nếu muốn hiển thị tên)
class CommentWithAuthor(CommentResponse):
    author_username: Optional[str] = None
```

---

## 6. CRUD Operations (`app/modules/comments/crud.py`)

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from .models import Comment
from .schemas import CommentCreate, CommentUpdate

# ========== CREATE ==========
async def create_comment(
    db: AsyncSession, 
    comment_data: CommentCreate, 
    post_id: int,
    author_id: int
) -> Comment:
    """Tạo comment mới cho bài viết"""
    db_comment = Comment(
        content=comment_data.content,
        post_id=post_id,
        author_id=author_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

# ========== READ (Single) ==========
async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Optional[Comment]:
    """Lấy comment theo ID"""
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    return result.scalars().first()

# ========== READ (List by Post) ==========
async def get_comments_by_post(
    db: AsyncSession, 
    post_id: int,
    skip: int = 0,
    limit: int = 20
) -> List[Comment]:
    """
    Lấy danh sách comments của một bài viết.
    Sắp xếp theo thời gian tạo (cũ nhất trước)
    """
    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def count_comments_by_post(db: AsyncSession, post_id: int) -> int:
    """Đếm số comment của một bài viết"""
    result = await db.execute(
        select(func.count(Comment.id)).where(Comment.post_id == post_id)
    )
    return result.scalar()

# ========== READ (List by Author) ==========
async def get_comments_by_author(db: AsyncSession, author_id: int) -> List[Comment]:
    """Lấy tất cả comments của một user"""
    result = await db.execute(
        select(Comment)
        .where(Comment.author_id == author_id)
        .order_by(Comment.created_at.desc())
    )
    return result.scalars().all()

# ========== UPDATE ==========
async def update_comment(
    db: AsyncSession, 
    comment_id: int, 
    comment_data: CommentUpdate
) -> Optional[Comment]:
    """Cập nhật nội dung comment"""
    db_comment = await get_comment_by_id(db, comment_id)
    if not db_comment:
        return None
    
    update_data = comment_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)
    
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

# ========== DELETE ==========
async def delete_comment(db: AsyncSession, comment_id: int) -> bool:
    """Xóa comment"""
    db_comment = await get_comment_by_id(db, comment_id)
    if not db_comment:
        return False
    
    await db.delete(db_comment)
    await db.commit()
    return True

async def delete_comments_by_post(db: AsyncSession, post_id: int) -> int:
    """Xóa tất cả comments của một bài viết (khi xóa bài)"""
    result = await db.execute(
        select(Comment).where(Comment.post_id == post_id)
    )
    comments = result.scalars().all()
    count = len(comments)
    
    for comment in comments:
        await db.delete(comment)
    
    await db.commit()
    return count
```

---

## 7. API Router (`app/modules/comments/router.py`)

```python
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from app.core.dependencies import DbSession, CurrentUser
from app.modules.posts import crud as post_crud
from . import crud, schemas

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])

# ========== PUBLIC ENDPOINTS ==========

@router.get("/", response_model=List[schemas.CommentResponse])
async def list_comments(
    db: DbSession,
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Lấy danh sách comments của một bài viết.
    Endpoint Public - không cần đăng nhập.
    """
    # Kiểm tra bài viết tồn tại
    post = await post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comments = await crud.get_comments_by_post(db, post_id, skip, limit)
    return comments

@router.get("/count")
async def count_comments(db: DbSession, post_id: int):
    """Đếm số comments của bài viết"""
    post = await post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    count = await crud.count_comments_by_post(db, post_id)
    return {"post_id": post_id, "comment_count": count}

# ========== PROTECTED ENDPOINTS ==========

@router.post("/", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    db: DbSession,
    current_user: CurrentUser,
    post_id: int,
    comment_data: schemas.CommentCreate
):
    """
    Thêm comment vào bài viết.
    Yêu cầu: Đăng nhập.
    """
    # Kiểm tra bài viết tồn tại
    post = await post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Chỉ cho comment bài đã publish
    if not post.is_published:
        raise HTTPException(status_code=400, detail="Cannot comment on unpublished post")
    
    comment = await crud.create_comment(
        db, 
        comment_data, 
        post_id=post_id, 
        author_id=current_user.id
    )
    return comment

@router.put("/{comment_id}", response_model=schemas.CommentResponse)
async def update_comment(
    db: DbSession,
    current_user: CurrentUser,
    post_id: int,
    comment_id: int,
    comment_data: schemas.CommentUpdate
):
    """
    Sửa comment.
    Yêu cầu: Đăng nhập và là chủ comment.
    """
    comment = await crud.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Kiểm tra comment thuộc đúng post
    if comment.post_id != post_id:
        raise HTTPException(status_code=400, detail="Comment does not belong to this post")
    
    # Kiểm tra quyền sở hữu
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
    
    updated = await crud.update_comment(db, comment_id, comment_data)
    return updated

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    db: DbSession,
    current_user: CurrentUser,
    post_id: int,
    comment_id: int
):
    """
    Xóa comment.
    Yêu cầu: Đăng nhập và là chủ comment HOẶC là tác giả bài viết.
    """
    comment = await crud.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.post_id != post_id:
        raise HTTPException(status_code=400, detail="Comment does not belong to this post")
    
    # Cho phép xóa nếu: Là chủ comment HOẶC là tác giả bài viết
    post = await post_crud.get_post_by_id(db, post_id)
    is_comment_author = comment.author_id == current_user.id
    is_post_author = post.author_id == current_user.id
    
    if not (is_comment_author or is_post_author):
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    await crud.delete_comment(db, comment_id)
    return None
```

---

## 8. Router riêng cho User's Comments

**File: `app/modules/comments/user_router.py`** (Optional)

```python
from fastapi import APIRouter
from typing import List
from app.core.dependencies import DbSession, CurrentUser
from . import crud, schemas

router = APIRouter(prefix="/me/comments", tags=["My Comments"])

@router.get("/", response_model=List[schemas.CommentResponse])
async def get_my_comments(db: DbSession, current_user: CurrentUser):
    """Lấy tất cả comments của user hiện tại"""
    comments = await crud.get_comments_by_author(db, current_user.id)
    return comments
```

---

## 9. Đăng ký Router vào Main App

**File: `app/main.py`** (Cập nhật)

```python
from fastapi import FastAPI
from app.modules.users.router import router as user_router
from app.modules.auth.router import router as auth_router
from app.modules.posts.router import router as posts_router
from app.modules.comments.router import router as comments_router  # THÊM

app = FastAPI(title="Professional Blog API")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)
app.include_router(comments_router)  # THÊM

@app.get("/")
def root():
    return {"message": "Health check"}
```

---

## 10. Tích hợp với Posts (Cascade Delete)

Khi xóa bài viết, cần xóa luôn tất cả comments. Cập nhật `posts/router.py`:

```python
# app/modules/posts/router.py
from app.modules.comments import crud as comment_crud  # THÊM

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    db: DbSession,
    current_user: CurrentUser,
    post_id: int
):
    post = await crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    # Xóa tất cả comments trước
    await comment_crud.delete_comments_by_post(db, post_id)
    
    await crud.delete_post(db, post_id)
    return None
```

---

## 11. API Endpoints Summary

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET | `/posts/{post_id}/comments/` | Lấy danh sách comments | ❌ |
| GET | `/posts/{post_id}/comments/count` | Đếm số comments | ❌ |
| POST | `/posts/{post_id}/comments/` | Thêm comment mới | ✅ |
| PUT | `/posts/{post_id}/comments/{id}` | Sửa comment | ✅ (Owner) |
| DELETE | `/posts/{post_id}/comments/{id}` | Xóa comment | ✅ (Owner/Post Author) |
| GET | `/me/comments/` | Lấy comments của mình | ✅ |

---

## 12. ACTION ITEMS

1. [ ] Tạo folder `app/modules/comments/`
2. [ ] Tạo file `app/modules/comments/__init__.py` (empty)
3. [ ] Tạo file `app/modules/comments/models.py`
4. [ ] Chạy Alembic migration để tạo bảng `comments`
5. [ ] Tạo file `app/modules/comments/schemas.py`
6. [ ] Tạo file `app/modules/comments/crud.py`
7. [ ] Tạo file `app/modules/comments/router.py`
8. [ ] Cập nhật `app/main.py` (thêm comments router)
9. [ ] Cập nhật `app/modules/posts/router.py` (cascade delete)
10. [ ] Test toàn bộ API qua Swagger UI

---

## 13. Testing Checklist

- [ ] Xem comments của bài viết (không đăng nhập)
- [ ] Thêm comment khi chưa đăng nhập -> Expect 401
- [ ] Thêm comment vào bài chưa publish -> Expect 400
- [ ] Sửa comment của người khác -> Expect 403
- [ ] Tác giả bài viết xóa comment của người khác -> Expect 204 (Cho phép)
- [ ] Xóa bài viết có comments -> Comments cũng bị xóa

---

**Hoàn thành Phase 3a**, bạn đã có hệ thống Blog hoàn chỉnh với:
- User Authentication
- Posts Management
- Comments System
- Proper Authorization (Phân quyền đúng chuẩn)
