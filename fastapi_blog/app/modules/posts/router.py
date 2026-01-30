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