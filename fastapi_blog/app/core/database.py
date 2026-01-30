from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Lấy URL từ file .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Tạo Engine kết nối Async
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"server_settings": {"search_path": "blog_db"}}
)

# Tạo Session Factory
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base Model
class Base(DeclarativeBase):
    pass

# Dependency lấy DB Session
async def get_db():
    async with SessionLocal() as session:
        yield session