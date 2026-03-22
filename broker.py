import aio_pika
from settings import settings

async def get_amqp_connection():
    return await aio_pika.connect_robust(settings.AMQP_URL)
