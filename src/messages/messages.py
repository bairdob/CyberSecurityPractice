from typing import Optional, Type

from sqlalchemy.orm import Session

from gost.GOST import GOST
from gost.utils import hex_to_bin_mult_64, bytes_to_string, string_to_bytes, leading_zeros_hex
from src.auth import User
from src.messages.constants import SUPER_SECRET_KEY
from src.messages.models import Message
from src.messages.schemas import MessageIn


def by_message_id(db: Session, message_id: int) -> Optional[Message]:
    return db.query(Message).join(User).filter(Message.message_id == message_id).first()


def all_messages(db: Session) -> list[Type[Message]]:
    return db.query(Message).all()


def decrypt(message: Message) -> str:
    gost = GOST()
    gost.set_key(SUPER_SECRET_KEY)
    gost.set_operation_mode(gost.CFB)
    gost.set_iv(hex_to_bin_mult_64(message.iv))
    gost.set_encrypted_msg(hex_to_bin_mult_64(message.encrypted_message))
    result = bytes_to_string(gost.decrypt()).replace('\x00', '')
    return result


def encrypt(message: MessageIn) -> tuple[str, str]:
    gost = GOST()
    gost.set_message(string_to_bytes(message.message_text))
    gost.set_key(SUPER_SECRET_KEY)
    gost.set_operation_mode(gost.CFB)
    ciphertext = leading_zeros_hex(gost.encrypt())
    iv = leading_zeros_hex(gost.get_iv())
    return ciphertext, iv
