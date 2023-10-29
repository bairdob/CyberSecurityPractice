from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models import User, UserResponse, Role, RoleResponse

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping")
async def ping():
    return 'pong'


# Get all users
@app.get("/users/", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/roles", response_model=list[RoleResponse])
def get_all_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles
