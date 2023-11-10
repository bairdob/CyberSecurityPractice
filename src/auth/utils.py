from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.auth.models import User
from src.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token, db: Session):
    # This doesn't provide any security at all
    # Check the next version
    user = verify_user_by_token(token, db)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user = fake_decode_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def verify_user(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    return user


def verify_user_by_token(token: str, db: Session):
    user = db.query(User).filter(User.username == token).first()
    return user
