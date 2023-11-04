from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User, UserResponse, Role, RoleResponse

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


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


@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


def verify_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    return user


def verify_user_by_token(token: str, db: Session):
    user = db.query(User).filter(User.username == token).first()
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


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
