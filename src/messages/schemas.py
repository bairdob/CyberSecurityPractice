from pydantic import BaseModel


class MessageResponse(BaseModel):
    message_id: int
    encrypted_message: str


class MessageDecryptedResponse(BaseModel):
    message_id: int
    decrypted_message: str


class MessageCreate(BaseModel):
    user_id: int
    encrypted_message: str
    iv: str


class MessageIn(BaseModel):
    message_text: str


class MessageOut(BaseModel):
    message_id: int
    encrypted_message: str
    decrypted_message: str
