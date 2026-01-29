from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from routers.todo_router import router as todo_router  # ← THÊM DÒNG NÀY
from database import engine, Base, SessionLocal
from dependencies import get_db

app = FastAPI(title="ToDo App with PostgreSQL")
# Tạo bảng nếu chưa tồn tại (dev only)
Base.metadata.create_all(bind=engine)

# Tái sử dụng dependency (best practice)
db_dependency = Annotated[Session, Depends(get_db)]

# Endpoint GET đầu tiên – lấy tất cả todos
# @app.get("/todos")
# async def read_all(db: db_dependency):
#     """
#     Lấy tất cả các ToDo từ database.
#     """
#     return db.query(Todos).all()
#
# @app.get("/")
# async def root():
#     return {"message": "Welcome to ToDo App API!"}
app.include_router(todo_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)