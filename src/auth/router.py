from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.utils import get_current_user, verify_user
from src.database import get_db
from src.auth.models import UserResponse, User

router = APIRouter()


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = verify_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = user.username
    response = RedirectResponse(url='/messages', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="authorization", value=f"Bearer {access_token}", httponly=True)

    return response
