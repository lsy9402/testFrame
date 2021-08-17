from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger


async def unicorn_exception_handler(request: Request, e: Exception):
    logger.exception(e)
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": repr(e)})
