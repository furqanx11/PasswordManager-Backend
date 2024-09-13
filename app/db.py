from tortoise import Tortoise
from app.config import settings

async def init():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections()
