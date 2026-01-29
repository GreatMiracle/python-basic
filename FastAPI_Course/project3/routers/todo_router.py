from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from curd.todo_crud import get_todos
from schemas import Todo

from dependencies import get_db

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=list[Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_todos(db, skip, limit)