# app/modules/posts/models.py
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from app.core.database import Base
import datetime

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "blog_db"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    author_id = Column(Integer, index=True)
    # Quan hệ với User sẽ xử lý ở tầng CRUD/Service thay vì dùng relationship
