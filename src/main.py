from pathlib import Path

from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.auth import router as auth_router
from src.database import get_db
from src.models import User, UserResponse, Role, RoleResponse

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])


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
