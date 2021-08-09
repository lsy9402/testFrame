import sys
from datetime import date
from time import perf_counter

from fastapi import FastAPI, Request
from loguru import logger
from uvicorn.protocols.utils import get_path_with_query_string

from api.public import public_router as public
from api.tools import tools_router as tools
from core.config import settings
from core.error import unicorn_exception_handler
from db.base import db, db_init, close_redis
from db.test_tools import checks_map, tools_map
from utils.ToolsUtil import load_test_module

app = FastAPI()


@app.middleware("http")
async def add_log(request: Request, call_next):
    user = request.client.host if request.client.host != "127.0.0.1" else settings.LOCALHOST
    path = get_path_with_query_string(request.scope)
    logger.success("{} startup- {}", user, path)
    start_time = perf_counter()
    try:
        res = await call_next(request)
    finally:
        end_time = perf_counter()
        logger.success("{} shutdown {} run_time:{}", user, path, end_time - start_time)
    return res


@app.on_event("startup")
async def load_db():
    logger.remove()
    logger.add(sys.stderr, level=settings.LOG_LEVEL)
    logger.add(
        settings.LOG_DIR.joinpath(f'{date.today().strftime("%Y_%m_%d")}.log'),
        level=settings.LOG_LEVEL
    )
    logger.level(settings.LOG_LEVEL)
    db_init()
    load_test_module()
    logger.info(tools_map)
    logger.info(checks_map)
    await db.connect()


@app.on_event("shutdown")
async def close_db():
    await db.disconnect()
    await close_redis()


app.add_exception_handler(Exception, unicorn_exception_handler)
app.include_router(public)
app.include_router(tools)
