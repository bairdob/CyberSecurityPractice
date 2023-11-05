from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(255), unique=True, nullable=False)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    register_date = Column(Date, nullable=False)
    role = relationship('Role', backref='users')


class UserResponse(BaseModel):
    user_id: int
    username: str
    role_id: int
    register_date: datetime
    disabled: bool | None = None


class RoleResponse(BaseModel):
    role_id: int
    role_name: str
