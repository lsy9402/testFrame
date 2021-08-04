from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


async def unicorn_exception_handler(request: Request, e: Exception):
    logger.exception(e)
    return JSONResponse(status_code=418, content={"detail": repr(e)})
