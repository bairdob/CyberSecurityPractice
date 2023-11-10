from fastapi import Request, Depends
from pygost.gost3411_12 import GOST341112
from sqlalchemy.orm import Session

from src.auth.constants import SALT
from src.auth.models import User, Password
from src.database import get_db


def get_by_token(db: Session, token: str):
    return db.query(User).filter(User.username == token).first()


def get_user_from_token(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("authorization").split()[-1]
    user = get_by_token(db, token)
    return user


def calc_hash_password(password: str, user: User) -> str:
    data = f"{user.user_id}_{user.register_date}_{SALT}_{password}"
    m = GOST341112(digest_size=256)
    m.update(data.encode('utf-8'))
    result = m.hexdigest()
    return result


def get_hashed_password(db: Session, user: User) -> str:
    result = db.query(Password).filter(Password.user_id == user.user_id).first()
    return result.hashed_password
