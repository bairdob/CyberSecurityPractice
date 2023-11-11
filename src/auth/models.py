from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
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
    totp_secret = Column(String, nullable=True)
    role = relationship('Role', backref='users')


class Password(Base):
    __tablename__ = 'hashed_passwords'
    password_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    hashed_password = Column(Text, nullable=False)
    user = relationship('User', backref='hashed_passwords')
