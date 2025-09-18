

import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

SMTP_SERVER = st.secrets["SMTP_SERVER"]
SMTP_PORT = st.secrets["SMTP_PORT"]
EMAIL_ORIGEM = st.secrets["EMAIL_ORIGEM"]
SENHA_EMAIL = st.secrets["SENHA_EMAIL"]

def enviar_email_feedback(destinatario, assunto, corpo_mensagem):
    try:
        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = destinatario
        msg.set_content(corpo_mensagem)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
