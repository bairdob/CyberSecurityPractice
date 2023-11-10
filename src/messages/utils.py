from src.auth import User
from src.auth.schemas import Roles
from src.messages.messages import decrypt
from src.messages.models import Message


def create_PDF(messages: Message, user: User):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(10, 30, f"User: {user.username}")
    pdf.ln(30)
    with pdf.table(col_widths=(5, 50, 50), text_align=("CENTER")) as table:
        for message in messages:
            row = table.row()
            decrypted_message = decrypt(message) if user.role_id == Roles.DECRYPTOR.value else "decryption not allowed for user"
            data_row = (str(message.message_id), message.encrypted_message, decrypted_message)
            for datum in data_row:
                row.cell(datum)
    return pdf.output()
