from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies.auth import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    CurrentUser,
    get_password_hash,
)
from src.core.models.session import StartedSession
from src.core.models.user import User
from src.core.schemas.auth import Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[StartedSession()],
)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if ACCESS_TOKEN_EXPIRE_MINUTES == 0:
        expires_minutes = 999999
    else:
        expires_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=expires_minutes)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def get_my_data(current_user: CurrentUser):
    resp = current_user.dict()
    resp.pop("hashed_password")
    return resp


@router.post("/register", response_model_exclude={"hashed_password"})
async def register_user(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    is_admin: bool = Query(False),
):
    if User.one(User.username == data.username):
        raise HTTPException(status_code=400, detail="User already exists")
    return User.insert(username=data.username, hashed_password=get_password_hash(data.password), is_admin=is_admin)
