from beanie import init_beanie
from jinja2 import Environment, PackageLoader, select_autoescape
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

import models

jinja2_env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape(),
)


class Settings(BaseSettings):
    DATABASE_URL: str


async def init_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client.db_name, document_models=models.__all__)
