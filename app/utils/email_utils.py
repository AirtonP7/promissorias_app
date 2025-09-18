import smtplib
from email.message import EmailMessage
import streamlit as st  # necessário para usar st.secrets

# ----------------------------
# Configuração usando Secrets
# ----------------------------
SMTP_SERVER = st.secrets["SMTP_SERVER"]
SMTP_PORT = int(st.secrets["SMTP_PORT"])  # converte para inteiro
EMAIL_ORIGEM = st.secrets["EMAIL_ORIGEM"]
SENHA_EMAIL = st.secrets["SENHA_EMAIL"]

def enviar_email_feedback(destinatario: str, assunto: str, corpo_mensagem: str) -> bool:
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
