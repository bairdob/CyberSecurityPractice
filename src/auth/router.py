from typing import Annotated

import pyotp
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth import users
from src.auth.models import User
from src.auth.schemas import CreateUser, UserResponse
from src.auth.utils import get_current_user, verify_user
from src.database import get_db

router = APIRouter()


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = verify_user(form_data.username, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed_password = users.calc_hash_password(form_data.password, user)
    if hashed_password != users.get_hashed_password(db, user):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    totp_code = pyotp.TOTP(user.totp_secret).now()
    if totp_code != form_data.client_secret:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = user.username

    return {"access_token": access_token, "token_type": "bearer"}
