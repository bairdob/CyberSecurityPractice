from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models import User, UserResponse, Role, RoleResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


def verify_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    return user


def verify_user_by_token(token: str, db: Session):
    user = db.query(User).filter(User.username == token).first()
    # user = TypeAdapter(UserResponse).validate_python(user)
    return user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = verify_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/ping")
async def ping():
    return 'pong'


# Get all users
@app.get("/users", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/roles", response_model=list[RoleResponse])
def get_all_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles
