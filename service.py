import json
from dataclasses import dataclass

import aio_pika

from client import MailClient
from schemas import UserMessageBody
from broker import get_amqp_connection


@dataclass
class MailService:
    mail_client: MailClient


    async def consume_mail(self, message:aio_pika.IncomingMessage):
        print(message)
        async with message.process():
            try:
                print(message.body.decode())
                email_body= UserMessageBody(**json.loads(message.body.decode()))
                print("Sending email to:", email_body.user_email)
                correlation_id = message.correlation_id
                await self.send_welcome(subject=email_body.subject,text=email_body.message,to=email_body.user_email)
                raise ValueError("Test fail callback")
                print("Email sent successfully")
            except Exception as e:
                print("No way, bug again", e)
                try:
                    await self.send_mail_fail_callback(email=email_body.user_email,correlation_id=correlation_id,exception=e)
                    print("PUBLISHING CALLBACK")
                except Exception as callback_error:
                    print("Callback func failed itself", callback_error)



    async def send_welcome(self,subject: str, text: str, to: str):
        await self.mail_client.send_email_task(subject,text,to)

    async def send_mail_fail_callback(self,email:str, correlation_id: str, exception: Exception) -> None:
        connection = await get_amqp_connection()
        channel = await connection.channel()

        await channel.declare_queue(
            "callback_mail_queue",
            durable=True
        )

        message = aio_pika.Message(
            body= f"User_email: {email} failed with exception {exception}".encode(),
            correlation_id=correlation_id,
        )
        await channel.default_exchange.publish(
            message=message,
            routing_key='callback_mail_queue'  # exchanger in Rabbit have to understand which queue to use
        )

        return

