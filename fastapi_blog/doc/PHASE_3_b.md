# GIAI ĐOẠN 3b: KỸ THUẬT QUERY NÂNG CAO (Advanced Query Techniques)

Tài liệu này trình bày **các kỹ thuật query khác nhau** trong SQLAlchemy, sử dụng module Comments làm ví dụ thực tế. Từ cơ bản đến nâng cao, giúp bạn làm chủ mọi tình huống query phức tạp.

---

## Mục lục
1. [ORM Select cơ bản](#1-orm-select-cơ-bản)
2. [JOIN - Kết hợp nhiều bảng](#2-join---kết-hợp-nhiều-bảng)
3. [Subquery - Query lồng](#3-subquery---query-lồng)
4. [CTE - Common Table Expression](#4-cte---common-table-expression)
5. [Raw SQL với text()](#5-raw-sql-với-text)
6. [Aggregate Functions - Hàm thống kê](#6-aggregate-functions---hàm-thống-kê)
7. [Window Functions - Hàm cửa sổ](#7-window-functions---hàm-cửa-sổ)
8. [Dynamic Query Building](#8-dynamic-query-building)
9. [Pagination nâng cao](#9-pagination-nâng-cao)
10. [Performance Tips](#10-performance-tips)

---

## 1. ORM Select cơ bản

### 1.1. Select đơn giản
```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Lấy tất cả comments
async def get_all_comments(db: AsyncSession):
    result = await db.execute(select(Comment))
    return result.scalars().all()

# Lấy comment theo ID
async def get_comment_by_id(db: AsyncSession, comment_id: int):
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    return result.scalars().first()
```

### 1.2. Filtering với nhiều điều kiện
```python
from sqlalchemy import and_, or_, not_

# AND: Tất cả điều kiện phải đúng
async def get_recent_comments_by_post(db: AsyncSession, post_id: int, days: int = 7):
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(Comment).where(
            and_(
                Comment.post_id == post_id,
                Comment.created_at >= cutoff
            )
        )
    )
    return result.scalars().all()

# OR: Một trong các điều kiện đúng
async def get_comments_by_posts(db: AsyncSession, post_ids: list[int]):
    result = await db.execute(
        select(Comment).where(
            or_(*[Comment.post_id == pid for pid in post_ids])
        )
    )
    return result.scalars().all()

# IN: Kiểm tra giá trị trong danh sách (Cách gọn hơn OR)
async def get_comments_by_posts_v2(db: AsyncSession, post_ids: list[int]):
    result = await db.execute(
        select(Comment).where(Comment.post_id.in_(post_ids))
    )
    return result.scalars().all()

# NOT IN: Loại trừ
async def get_comments_except_posts(db: AsyncSession, excluded_post_ids: list[int]):
    result = await db.execute(
        select(Comment).where(Comment.post_id.not_in(excluded_post_ids))
    )
    return result.scalars().all()

# LIKE: Tìm kiếm text
async def search_comments(db: AsyncSession, keyword: str):
    result = await db.execute(
        select(Comment).where(
            Comment.content.ilike(f"%{keyword}%")  # Case-insensitive
        )
    )
    return result.scalars().all()
```

### 1.3. Ordering (Sắp xếp)
```python
from sqlalchemy import desc, asc, nullslast

# Sắp xếp đơn giản
async def get_comments_newest_first(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(desc(Comment.created_at))  # Mới nhất trước
    )
    return result.scalars().all()

# Sắp xếp nhiều cột
async def get_comments_ordered(db: AsyncSession):
    result = await db.execute(
        select(Comment)
        .order_by(
            Comment.post_id.asc(),           # Theo post_id tăng dần
            Comment.created_at.desc()         # Trong cùng post, mới nhất trước
        )
    )
    return result.scalars().all()
```

---

## 2. JOIN - Kết hợp nhiều bảng

### 2.1. INNER JOIN (Chỉ lấy records khớp cả 2 bảng)
```python
from sqlalchemy import select
from app.modules.comments.models import Comment
from app.modules.posts.models import Post
from app.modules.users.models import User

# Lấy comments kèm thông tin post
async def get_comments_with_post(db: AsyncSession):
    result = await db.execute(
        select(Comment, Post.title)
        .join(Post, Comment.post_id == Post.id)
    )
    # Trả về list of tuples: [(Comment, "Post Title"), ...]
    return result.all()

# Lấy comments kèm thông tin author
async def get_comments_with_author(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(Comment, User.username)
        .join(User, Comment.author_id == User.id)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
    )
    
    # Chuyển thành list of dict cho dễ dùng
    comments = []
    for comment, username in result.all():
        comments.append({
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at,
            "author_username": username
        })
    return comments
```

### 2.2. LEFT JOIN (Lấy tất cả từ bảng trái, kể cả không khớp)
```python
from sqlalchemy import select, func
from sqlalchemy.orm import aliased

# Lấy tất cả posts, kể cả posts không có comment
async def get_posts_with_comment_count(db: AsyncSession):
    result = await db.execute(
        select(
            Post,
            func.count(Comment.id).label("comment_count")
        )
        .outerjoin(Comment, Post.id == Comment.post_id)  # LEFT OUTER JOIN
        .group_by(Post.id)
        .order_by(desc("comment_count"))
    )
    
    posts = []
    for post, count in result.all():
        posts.append({
            "id": post.id,
            "title": post.title,
            "comment_count": count
        })
    return posts
```

### 2.3. Multiple JOINs (Join nhiều bảng)
```python
# Lấy comments với thông tin cả post và author
async def get_comments_full_info(db: AsyncSession, limit: int = 50):
    result = await db.execute(
        select(
            Comment.id,
            Comment.content,
            Comment.created_at,
            Post.title.label("post_title"),
            Post.slug.label("post_slug"),
            User.username.label("author_name")
        )
        .join(Post, Comment.post_id == Post.id)
        .join(User, Comment.author_id == User.id)
        .order_by(desc(Comment.created_at))
        .limit(limit)
    )
    return result.mappings().all()  # List of dict-like objects
```

### 2.4. Self JOIN (Join với chính bảng đó)
```python
# Ví dụ: Nếu có reply_to_id cho nested comments
# Lấy comment và comment cha của nó

async def get_comment_with_parent(db: AsyncSession, comment_id: int):
    ParentComment = aliased(Comment)  # Tạo alias
    
    result = await db.execute(
        select(
            Comment,
            ParentComment.content.label("parent_content")
        )
        .outerjoin(ParentComment, Comment.reply_to_id == ParentComment.id)
        .where(Comment.id == comment_id)
    )
    return result.first()
```

---

## 3. Subquery - Query lồng

### 3.1. Subquery trong WHERE
```python
from sqlalchemy import select, func

# Lấy posts có nhiều hơn 10 comments
async def get_popular_posts(db: AsyncSession, min_comments: int = 10):
    # Subquery: Tính số comments cho mỗi post
    subq = (
        select(Comment.post_id, func.count(Comment.id).label("cnt"))
        .group_by(Comment.post_id)
        .having(func.count(Comment.id) >= min_comments)
        .subquery()
    )
    
    # Query chính
    result = await db.execute(
        select(Post)
        .join(subq, Post.id == subq.c.post_id)
    )
    return result.scalars().all()
```

### 3.2. Scalar Subquery (Subquery trả về 1 giá trị)
```python
from sqlalchemy import select, func

# Lấy post mới nhất của mỗi user
async def get_latest_post_per_user(db: AsyncSession):
    # Scalar subquery: Lấy max created_at cho mỗi author
    latest = (
        select(func.max(Post.created_at))
        .where(Post.author_id == User.id)
        .correlate(User)
        .scalar_subquery()
    )
    
    result = await db.execute(
        select(User, Post)
        .join(Post, and_(
            Post.author_id == User.id,
            Post.created_at == latest
        ))
    )
    return result.all()
```

### 3.3. EXISTS Subquery
```python
from sqlalchemy import select, exists

# Lấy users đã từng comment
async def get_users_who_commented(db: AsyncSession):
    comment_exists = (
        select(Comment.id)
        .where(Comment.author_id == User.id)
        .exists()
    )
    
    result = await db.execute(
        select(User).where(comment_exists)
    )
    return result.scalars().all()

# Lấy posts CHƯA có comment nào
async def get_posts_without_comments(db: AsyncSession):
    has_comments = (
        select(Comment.id)
        .where(Comment.post_id == Post.id)
        .exists()
    )
    
    result = await db.execute(
        select(Post).where(~has_comments)  # ~ là NOT
    )
    return result.scalars().all()
```

---

## 4. CTE - Common Table Expression

CTE giúp chia query phức tạp thành nhiều phần dễ đọc.

### 4.1. CTE cơ bản
```python
from sqlalchemy import select, func, literal_column

async def get_engagement_report(db: AsyncSession):
    # CTE 1: Đếm posts của mỗi user
    post_counts = (
        select(
            Post.author_id.label("user_id"),
            func.count(Post.id).label("post_count")
        )
        .group_by(Post.author_id)
        .cte("post_counts")
    )
    
    # CTE 2: Đếm comments của mỗi user
    comment_counts = (
        select(
            Comment.author_id.label("user_id"),
            func.count(Comment.id).label("comment_count")
        )
        .group_by(Comment.author_id)
        .cte("comment_counts")
    )
    
    # Query chính: Kết hợp các CTE
    result = await db.execute(
        select(
            User.id,
            User.username,
            func.coalesce(post_counts.c.post_count, 0).label("posts"),
            func.coalesce(comment_counts.c.comment_count, 0).label("comments")
        )
        .outerjoin(post_counts, User.id == post_counts.c.user_id)
        .outerjoin(comment_counts, User.id == comment_counts.c.user_id)
        .order_by(desc("posts"))
    )
    return result.mappings().all()
```

### 4.2. Recursive CTE (Cho nested comments/categories)
```python
# Ví dụ: Lấy tất cả reply của một comment (multi-level)
# Giả sử Comment có field reply_to_id

async def get_comment_thread(db: AsyncSession, root_comment_id: int):
    # Đây là cách viết recursive CTE trong SQLAlchemy
    comment_tree = (
        select(
            Comment.id,
            Comment.content,
            Comment.reply_to_id,
            literal_column("1").label("level")
        )
        .where(Comment.id == root_comment_id)
        .cte("comment_tree", recursive=True)
    )
    
    # Phần đệ quy
    comment_alias = aliased(Comment)
    comment_tree = comment_tree.union_all(
        select(
            comment_alias.id,
            comment_alias.content,
            comment_alias.reply_to_id,
            (comment_tree.c.level + 1).label("level")
        )
        .join(comment_tree, comment_alias.reply_to_id == comment_tree.c.id)
    )
    
    result = await db.execute(
        select(comment_tree)
        .order_by(comment_tree.c.level, comment_tree.c.id)
    )
    return result.mappings().all()
```

---

## 5. Raw SQL với text()

Khi ORM quá phức tạp hoặc cần tối ưu hiệu năng.

### 5.1. Raw SQL cơ bản
```python
from sqlalchemy import text

async def raw_get_comments_stats(db: AsyncSession):
    sql = text("""
        SELECT 
            p.id as post_id,
            p.title,
            COUNT(c.id) as comment_count,
            MAX(c.created_at) as last_comment_at,
            MIN(c.created_at) as first_comment_at
        FROM blog_db.posts p
        LEFT JOIN blog_db.comments c ON p.id = c.post_id
        WHERE p.is_published = true
        GROUP BY p.id, p.title
        HAVING COUNT(c.id) > 0
        ORDER BY comment_count DESC
        LIMIT 20
    """)
    
    result = await db.execute(sql)
    return result.mappings().all()
```

### 5.2. Raw SQL với Parameters (Tránh SQL Injection!)
```python
async def raw_search_comments(db: AsyncSession, keyword: str, post_id: int = None):
    # LUÔN DÙNG PARAMETERS, KHÔNG BAO GIỜ FORMAT STRING!
    sql = text("""
        SELECT 
            c.id,
            c.content,
            c.created_at,
            u.username as author_name,
            p.title as post_title
        FROM blog_db.comments c
        JOIN blog_db.users u ON c.author_id = u.id
        JOIN blog_db.posts p ON c.post_id = p.id
        WHERE 
            c.content ILIKE :keyword
            AND (:post_id IS NULL OR c.post_id = :post_id)
        ORDER BY c.created_at DESC
        LIMIT 50
    """)
    
    result = await db.execute(sql, {
        "keyword": f"%{keyword}%",
        "post_id": post_id
    })
    return result.mappings().all()
```

### 5.3. Raw SQL với PostgreSQL-specific features
```python
# Full-text search với PostgreSQL
async def fulltext_search_comments(db: AsyncSession, search_query: str):
    sql = text("""
        SELECT 
            c.id,
            c.content,
            c.created_at,
            ts_rank(
                to_tsvector('simple', c.content),
                plainto_tsquery('simple', :query)
            ) as relevance
        FROM blog_db.comments c
        WHERE to_tsvector('simple', c.content) @@ plainto_tsquery('simple', :query)
        ORDER BY relevance DESC
        LIMIT 20
    """)
    
    result = await db.execute(sql, {"query": search_query})
    return result.mappings().all()

# JSON aggregation (PostgreSQL)
async def get_posts_with_comments_json(db: AsyncSession):
    sql = text("""
        SELECT 
            p.id,
            p.title,
            p.slug,
            COALESCE(
                json_agg(
                    json_build_object(
                        'id', c.id,
                        'content', c.content,
                        'author_id', c.author_id,
                        'created_at', c.created_at
                    ) ORDER BY c.created_at
                ) FILTER (WHERE c.id IS NOT NULL),
                '[]'::json
            ) as comments
        FROM blog_db.posts p
        LEFT JOIN blog_db.comments c ON p.id = c.post_id
        WHERE p.is_published = true
        GROUP BY p.id
        ORDER BY p.created_at DESC
    """)
    
    result = await db.execute(sql)
    return result.mappings().all()
```

---

## 6. Aggregate Functions - Hàm thống kê

### 6.1. Các hàm cơ bản
```python
from sqlalchemy import select, func

async def get_comment_statistics(db: AsyncSession):
    result = await db.execute(
        select(
            func.count(Comment.id).label("total_comments"),
            func.count(func.distinct(Comment.author_id)).label("unique_authors"),
            func.count(func.distinct(Comment.post_id)).label("commented_posts"),
            func.min(Comment.created_at).label("first_comment"),
            func.max(Comment.created_at).label("last_comment")
        )
    )
    return result.mappings().first()
```

### 6.2. GROUP BY với HAVING
```python
# Lấy top authors với nhiều comments nhất
async def get_top_commenters(db: AsyncSession, limit: int = 10, min_comments: int = 5):
    result = await db.execute(
        select(
            Comment.author_id,
            User.username,
            func.count(Comment.id).label("comment_count")
        )
        .join(User, Comment.author_id == User.id)
        .group_by(Comment.author_id, User.username)
        .having(func.count(Comment.id) >= min_comments)
        .order_by(desc("comment_count"))
        .limit(limit)
    )
    return result.mappings().all()
```

### 6.3. Thống kê theo thời gian
```python
from sqlalchemy import extract

# Đếm comments theo tháng
async def get_monthly_comment_stats(db: AsyncSession, year: int = 2024):
    result = await db.execute(
        select(
            extract("month", Comment.created_at).label("month"),
            func.count(Comment.id).label("count")
        )
        .where(extract("year", Comment.created_at) == year)
        .group_by("month")
        .order_by("month")
    )
    return result.mappings().all()

# Đếm comments theo ngày trong tuần
async def get_weekday_stats(db: AsyncSession):
    result = await db.execute(
        select(
            extract("dow", Comment.created_at).label("day_of_week"),  # 0=Sun, 6=Sat
            func.count(Comment.id).label("count")
        )
        .group_by("day_of_week")
        .order_by("day_of_week")
    )
    return result.mappings().all()
```

---

## 7. Window Functions - Hàm cửa sổ

Window functions rất mạnh cho ranking, running totals, etc.

### 7.1. ROW_NUMBER, RANK
```python
from sqlalchemy import select, func, over

# Đánh số thứ tự comments trong mỗi post
async def get_comments_with_rank(db: AsyncSession, post_id: int):
    row_num = func.row_number().over(
        partition_by=Comment.post_id,
        order_by=Comment.created_at
    ).label("comment_number")
    
    result = await db.execute(
        select(Comment, row_num)
        .where(Comment.post_id == post_id)
    )
    return result.all()

# Xếp hạng users theo số comments
async def rank_users_by_comments(db: AsyncSession):
    subq = (
        select(
            Comment.author_id,
            func.count(Comment.id).label("comment_count")
        )
        .group_by(Comment.author_id)
        .subquery()
    )
    
    rank = func.rank().over(
        order_by=desc(subq.c.comment_count)
    ).label("rank")
    
    result = await db.execute(
        select(
            User.username,
            subq.c.comment_count,
            rank
        )
        .join(subq, User.id == subq.c.author_id)
    )
    return result.mappings().all()
```

### 7.2. Running Total, Moving Average
```python
# Tổng dồn comments theo ngày
async def get_cumulative_comments(db: AsyncSession):
    sql = text("""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as daily_count,
            SUM(COUNT(*)) OVER (ORDER BY DATE(created_at)) as cumulative_count
        FROM blog_db.comments
        GROUP BY DATE(created_at)
        ORDER BY date
    """)
    
    result = await db.execute(sql)
    return result.mappings().all()

# Moving average 7 ngày
async def get_moving_average_comments(db: AsyncSession):
    sql = text("""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as daily_count,
            AVG(COUNT(*)) OVER (
                ORDER BY DATE(created_at)
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ) as avg_7_days
        FROM blog_db.comments
        GROUP BY DATE(created_at)
        ORDER BY date
    """)
    
    result = await db.execute(sql)
    return result.mappings().all()
```

---

## 8. Dynamic Query Building

Xây dựng query linh hoạt dựa trên input.

### 8.1. Filter Builder
```python
from sqlalchemy import select, and_
from typing import Optional
from datetime import datetime

async def search_comments_dynamic(
    db: AsyncSession,
    post_id: Optional[int] = None,
    author_id: Optional[int] = None,
    keyword: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 20
):
    query = select(Comment)
    
    # Build filters dynamically
    filters = []
    
    if post_id is not None:
        filters.append(Comment.post_id == post_id)
    
    if author_id is not None:
        filters.append(Comment.author_id == author_id)
    
    if keyword:
        filters.append(Comment.content.ilike(f"%{keyword}%"))
    
    if from_date:
        filters.append(Comment.created_at >= from_date)
    
    if to_date:
        filters.append(Comment.created_at <= to_date)
    
    # Apply all filters
    if filters:
        query = query.where(and_(*filters))
    
    # Pagination
    query = query.order_by(desc(Comment.created_at)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()
```

### 8.2. Dynamic Ordering
```python
from sqlalchemy import asc, desc

async def get_comments_sorted(
    db: AsyncSession,
    post_id: int,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    query = select(Comment).where(Comment.post_id == post_id)
    
    # Validate và áp dụng sorting
    allowed_columns = {
        "created_at": Comment.created_at,
        "updated_at": Comment.updated_at,
        "id": Comment.id
    }
    
    column = allowed_columns.get(sort_by, Comment.created_at)
    order_func = desc if sort_order == "desc" else asc
    
    query = query.order_by(order_func(column))
    
    result = await db.execute(query)
    return result.scalars().all()
```

---

## 9. Pagination nâng cao

### 9.1. Offset-based (Cách phổ biến)
```python
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

async def get_comments_paginated(
    db: AsyncSession,
    post_id: int,
    page: int = 1,
    size: int = 20
) -> dict:
    # Count total
    total = await db.execute(
        select(func.count(Comment.id)).where(Comment.post_id == post_id)
    )
    total_count = total.scalar()
    
    # Get items
    offset = (page - 1) * size
    items_result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .offset(offset)
        .limit(size)
    )
    items = items_result.scalars().all()
    
    return {
        "items": items,
        "total": total_count,
        "page": page,
        "size": size,
        "pages": (total_count + size - 1) // size  # Ceiling division
    }
```

### 9.2. Cursor-based (Hiệu năng cao hơn cho dữ liệu lớn)
```python
from datetime import datetime
from typing import Optional

async def get_comments_cursor(
    db: AsyncSession,
    post_id: int,
    cursor: Optional[datetime] = None,  # created_at của comment cuối cùng
    limit: int = 20
):
    query = select(Comment).where(Comment.post_id == post_id)
    
    if cursor:
        query = query.where(Comment.created_at > cursor)
    
    query = query.order_by(Comment.created_at.asc()).limit(limit + 1)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    has_more = len(items) > limit
    if has_more:
        items = items[:limit]
    
    return {
        "items": items,
        "next_cursor": items[-1].created_at.isoformat() if items else None,
        "has_more": has_more
    }
```

---

## 10. Performance Tips

### 10.1. Chỉ select columns cần thiết
```python
# ❌ Không tốt: Lấy tất cả columns
result = await db.execute(select(Comment))

# ✅ Tốt hơn: Chỉ lấy columns cần
result = await db.execute(
    select(Comment.id, Comment.content, Comment.created_at)
)
```

### 10.2. Sử dụng Index
```python
# Đảm bảo có index trên các columns thường filter
class Comment(Base):
    __tablename__ = "comments"
    
    post_id = Column(Integer, index=True)      # Index!
    author_id = Column(Integer, index=True)    # Index!
    created_at = Column(DateTime, index=True)  # Index cho sorting
```

### 10.3. Avoid N+1 Query
```python
# ❌ N+1 Problem
posts = await get_all_posts(db)
for post in posts:
    comments = await get_comments_by_post(db, post.id)  # Query mỗi post!

# ✅ Single query với JOIN hoặc subquery
posts_with_counts = await get_posts_with_comment_count(db)
```

### 10.4. Sử dụng EXPLAIN ANALYZE (Debug)
```python
# In ra query plan để tối ưu
async def debug_query(db: AsyncSession):
    sql = text("EXPLAIN ANALYZE SELECT * FROM blog_db.comments WHERE post_id = 1")
    result = await db.execute(sql)
    for row in result:
        print(row)
```

---

## Tổng kết: Chọn cách nào?

| Tình huống | Cách tiếp cận |
|------------|---------------|
| CRUD đơn giản | ORM `select()` |
| Lấy data từ nhiều bảng | `join()` |
| So sánh với kết quả khác | Subquery |
| Query phức tạp, dễ đọc | CTE |
| Full-text search, JSON | Raw SQL |
| Thống kê, báo cáo | Aggregate + GROUP BY |
| Ranking, running total | Window Functions |
| API với nhiều filter | Dynamic Query Building |

---

**Lời khuyên cuối:**
1. Bắt đầu với ORM, chuyển sang Raw SQL khi cần
2. Luôn test hiệu năng với `EXPLAIN ANALYZE`
3. Đặt index cho columns thường query
4. Sử dụng cursor pagination cho dữ liệu lớn
