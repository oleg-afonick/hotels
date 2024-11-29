import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from src.config import settings



def send_email(subject: str, body: str, recipient: str):
    if settings.EMAIL_BACKEND == "smtp":
        sender_email = settings.SENDER_EMAIL
        sender_password = settings.SENDER_PASSWORD
        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT_SSL if settings.USE_SSL else settings.SMTP_PORT_TLS

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "text/plain"))

        try:
            if settings.USE_SSL:
                # Если используется SSL, то используем smtplib.SMTP_SSL
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient, message.as_string())
            else:
                # Если используется TLS, то стандартный SMTP и starttls()
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()  # Начинаем TLS-соединение
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient, message.as_string())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка отправки письма: {e}")

    elif settings.EMAIL_BACKEND == "console":
        print(f"=== Email to {recipient} ===")
        print(f"Subject: {subject}")
        print(f"Message: {body}")
        print("=============================")
