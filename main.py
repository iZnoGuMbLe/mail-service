from contextlib import asynccontextmanager

from fastapi import FastAPI

from settings import settings
from utils import make_amqp_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_amqp_connection()
    yield


app = FastAPI(lifespan=lifespan)