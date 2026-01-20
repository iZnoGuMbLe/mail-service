import aio_pika
from settings import Settings

async def get_amqp_connection():
    settings = Settings()
    return await aio_pika.connect_robust(settings.AMQP_URL)
