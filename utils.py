import aio_pika

from client import MailClient
from service import MailService
from settings import settings
from broker import get_amqp_connection


async def get_mail_service() -> MailService:              #make dependecies in same file cuz service isn't big enough
    return MailService(
        mail_client=MailClient()
    )


async def make_amqp_connection():
    mail_service = await get_mail_service()
    connection = await get_amqp_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue('mail_queue', durable=True)
    await queue.consume(mail_service.consume_mail)