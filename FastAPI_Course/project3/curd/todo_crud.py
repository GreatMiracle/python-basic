from sqlalchemy.orm import Session
from models import (Todos)


def get_todos(db: Session, skip: int = 2, limit: int = 4):
    return db.query(Todos).offset(skip).limit(limit).all()