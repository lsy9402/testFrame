from datetime import date

from fastapi import FastAPI
from loguru import logger

from api.public import public_router as public
from core.config import settings
from core.error import unicorn_exception_handler
from db.base import db, db_init

app = FastAPI()


@app.on_event("startup")
async def load_db():
    logger.add(
        settings.LOG_DIR.joinpath(f'{date.today().strftime("%Y_%m_%d")}.log'),
        level=settings.LOG_LEVEL
    )
    db_init()
    await db.connect()


@app.on_event("shutdown")
async def close_db():
    await db.disconnect()


app.add_exception_handler(Exception, unicorn_exception_handler)
app.include_router(public)
