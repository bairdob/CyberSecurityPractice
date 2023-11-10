from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from fastapi import Form
from pydantic import BaseModel


@dataclass
class CreateUser:
    username: str = Form(...)
    password: str = Form(...)
    role_id: int = Form(...)


class UserResponse(BaseModel):
    user_id: int
    username: str
    role_id: int
    register_date: datetime
    disabled: bool | None = None


class RoleResponse(BaseModel):
    role_id: int
    role_name: str


class Roles(Enum):
    VIEWER = 1
    ENCRYPTOR = 2
    DECRYPTOR = 3
