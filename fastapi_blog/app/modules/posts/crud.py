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