# app/modules/users/router.py
from fastapi import APIRouter, Depends, HTTPException
from . import crud, schemas
from app.core.dependencies import DbSession

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserResponse)  
async def create_user_api(user: schemas.UserCreate, db: DbSession):
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(db, user) 