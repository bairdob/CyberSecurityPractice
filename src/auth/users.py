from sqlalchemy.orm import Session
from fastapi import Request, Depends

from src.auth.models import User
from src.database import get_db


def get_by_token(db: Session, token: str):
    return db.query(User).filter(User.username == token).first()


def get_user_from_token(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("authorization").split()[-1]
    user = get_by_token(db, token)
    return user
