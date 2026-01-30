from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core import security
from app.modules.users import crud as user_crud
from app.modules.users.models import User

# Đã có từ trước
DbSession = Annotated[AsyncSession, Depends(get_db)]

# OAuth2 scheme để lấy token từ Header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency để lấy user hiện tại từ JWT Token.
    Raise 401 nếu token không hợp lệ.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Type Alias cho Current User (Giống DbSession)
CurrentUser = Annotated[User, Depends(get_current_user)]