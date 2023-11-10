from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.auth.users import get_user_from_token
from src.database import get_db
from src.messages import messages
from src.messages.models import Message
from src.messages.schemas import MessageResponse, MessageDecryptedResponse, MessageCreate, MessageIn

router = APIRouter()


@router.get("/messages", response_model=list[MessageResponse])
async def get_messages(db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    message = messages.all_messages(db, user)
    if not message:
        raise HTTPException(status_code=404, detail="Messages not found")

    return message


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    message = messages.by_message_id_and_user_id(db, message_id, user.user_id)
    if not message:
        raise HTTPException(status_code=404, detail=f"Message with 'message_id={message_id}' not found")

    return message


@router.get("/messages/{message_id}/decrypt", response_model=MessageDecryptedResponse)
async def decrypt_message(message_id: int, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    message = messages.by_message_id_and_user_id(db, message_id, user.user_id)
    if not message:
        raise HTTPException(status_code=404, detail=f"Message with 'message_id={message_id}' not found")

    return {
        "message_id": message.message_id,
        "decrypted_message": messages.decrypt(message)
    }


@router.post("/messages")
async def create_message(message: MessageIn, db: Session = Depends(get_db), user=Depends(get_user_from_token)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ciphertext, iv = messages.encrypt(message)
    db_message = MessageCreate(
        user_id=user.user_id, message_text=message.message_text, encrypted_message=ciphertext, iv=iv)

    db_message = Message(**db_message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message.encrypted_message
