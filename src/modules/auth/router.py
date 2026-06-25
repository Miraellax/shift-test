from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from . import schema as auth_schema
from ..users.repository import BaseUsersRepository, get_users_repository, schema as users_schema

SECRET_KEY = "09d25e094faa6csq7jcwnp6066b7a9f63b974709fx6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 10

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

async def get_user(users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)],
                   username: str,
                   ) -> users_schema.User:
    user = await users_repo.get_user_info_by_username(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Введен неверный логин или пароль")

    return users_schema.User.model_validate(user)

async def authenticate_user(username: str,
                            password: str,
                            users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                            ):
    user = await get_user(users_repo, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Введен неверный логин или пароль")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Введен неверный логин или пароль")
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                           ) -> users_schema.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить данные учетной записи",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth_schema.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(users_repo, token_data.username)
    return user


@router.get("/current", response_model=users_schema.UserPublicInfo)
async def get_current_user(current_user: Annotated[users_schema.UserPublicInfo, Depends(get_current_user)]):
    return current_user

@router.post("/login", response_model=auth_schema.Token | None)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                                 ) -> auth_schema.Token | None:
    user = await authenticate_user(users_repo=users_repo, username=form_data.username, password=form_data.password)

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return auth_schema.Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=auth_schema.Token | None)
async def register_user(username: str,
                        password: str,
                        is_admin: bool,
                        users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                        ) -> auth_schema.Token | None:
    check_user = await users_repo.get_user_info_by_username(username)
    if check_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Указанный логин уже занят",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hashed_password = get_password_hash(password)
    user_schema = users_schema.UserCreate(username=username, hashed_password=hashed_password, is_admin=is_admin)
    new_user = await users_repo.post_user(user_schema)

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    return auth_schema.Token(access_token=access_token, token_type="bearer")




