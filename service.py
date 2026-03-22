import json
from dataclasses import dataclass

import aio_pika

from client import MailClient
from schemas import UserMessageBody
from settings import settings


@dataclass
class MailService:
    mail_client: MailClient


    async def consume_mail(self, message:aio_pika.IncomingMessage):
        email_body = UserMessageBody(**json.loads(message.body.decode()))

        async with message.process():
            if email_body.type == "verification":
                link = f"{settings.BASE_URL}/verify-email?token={email_body.token}"
                subject = "Подтверждение email в приложении Daily TaskTracker"
                text = (
                      f"Привет, {email_body.username}!\n\n"
                      f"Добро пожаловать в Daily TaskTracker!\n\n"                                                                           
                      f"Для подтверждения вашего email перейдите по ссылке:\n"
                      f"{link}\n\n"                                                                                                     
                      f"Ссылка действительна 24 часа.\n\n"                                                                            
                      f"Если вы не создавали аккаунт в DailyTracker — просто проигнорируйте это письмо.\n\n"
                      f"С уважением,\nКоманда DailyTracker"
                )
                await self.mail_client.send_email_task(subject=subject,text=text, to=email_body.email)

            if email_body.type == "password recover":
                link = f"{settings.BASE_URL}/recover-email?token={email_body.token}"
                subject = "Создание нового пароля Daily TaskTracker"
                text = (
                  f"Привет, {email_body.username}!\n\n"
                  f"Добро пожаловать в Daily TaskTracker!\n\n"                                                                           
                  f"Для сброса пароля и создания нового перейдите по ссылке:\n"
                  f"{link}\n\n"                                                                                                     
                  f"Ссылка действительна 1 час.\n\n"                                                                            
                  f"Если вы не сбрасывали пароль в DailyTracker — просто проигнорируйте это письмо.\n\n"
                  f"С уважением,\nКоманда DailyTracker"
                )

                await self.mail_client.send_email_task(subject=subject, text=text, to=email_body.email)


