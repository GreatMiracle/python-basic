from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from app.modules.users import crud as user_crud 
from . import schemas
from app.core.dependencies import DbSession

router = APIRouter(tags=["Authentication"])

@router.post("/token", response_model=schemas.Token)
async def login(db: DbSession, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_crud.get_user_by_username(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}