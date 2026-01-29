
# todo_app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#
# # URL database SQLite – file todos.db sẽ được tạo trong thư mục hiện tại
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
#
# # Tạo engine – kết nối đến database
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False}  # Cần cho SQLite trong FastAPI (multi-thread)
# )
#
# # Tạo SessionLocal class – dùng để tạo session database trong các endpoint
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )
#
# # Base class – tất cả model (Todo, User...) sẽ kế thừa từ Base
# Base = declarative_base()


# URL kết nối PostgreSQL từ Docker Compose
# user: learn
# password: 123456a@
# host: db (tên service trong docker-compose)
# port: 5432 (mặc định)
# database: postgres (mặc định, hoặc bạn có thể tạo DB riêng)
SQLALCHEMY_DATABASE_URL = "postgresql://learn:123456a%40@localhost:5432/postgres"

# Tạo engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # Không cần check_same_thread với PostgreSQL
)

# Tạo SessionLocal – dùng để inject vào các endpoint
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho tất cả models
Base = declarative_base()