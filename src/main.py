from pathlib import Path

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.auth import router as auth_router
from src.auth import users
from src.auth.models import User, Role
from src.auth.schemas import UserResponse, RoleResponse
from src.database import get_db
from src.messages import router as messages_router
from src.messages.models import Message

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

app.include_router(auth_router.router, prefix="", tags=["Auth"])
app.include_router(messages_router.router, prefix="/api/v1", tags=["Messages"])


@app.get("/ping")
async def ping():
    return 'pong'


# Get all users
@app.get("/users", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users_data = db.query(User).offset(skip).limit(limit).all()
    return users_data


@app.get("/roles", response_model=list[RoleResponse])
def get_all_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles


@app.get("/")
async def index():
    # Redirect to the login route
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@app.get("/messages", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    token = request.headers.get("authorization").split()[-1]
    user = users.get_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return templates.TemplateResponse(
        name="messages.html",
        context={"request": request, "token": token, "messages": messages})
