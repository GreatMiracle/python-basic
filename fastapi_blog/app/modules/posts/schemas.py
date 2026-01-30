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