import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import Settings


class MailClient:

    def __init__(self):
        self.settings = Settings()

    async def send_email_task(self,subject: str, text: str, to: str):
        message = self._build_message(subject, text, to)
        await asyncio.to_thread(self._send_email,message)  # this func has to be async cuz it's being used in send_welcome func which is async.

    def _build_message(self,subject: str, text: str, to: str):
        message = MIMEMultipart()

        message["From"] = self.settings.from_email
        message["To"] = to
        message["Subject"] = subject
        message.attach( MIMEText(text, 'plain'))
        return message

    def _send_email(self,message: MIMEMultipart):
        server = smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT)
        server.send_message(message)
        server.quit()
