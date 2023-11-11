from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    encrypted_message = Column(Text, nullable=False)
    iv = Column(Text, nullable=False)
    user = relationship('User', backref='messages')
