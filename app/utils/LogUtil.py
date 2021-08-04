from functools import wraps
from time import perf_counter

from loguru import logger

from core.config import settings


def add_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get("req").client.host if kwargs.get("req").client.host != "127.0.0.1" else settings.LOCALHOST
        logger.success("{} startup~ {}", user, func.__name__)
        start_time = perf_counter()
        ret = await func(*args, **kwargs)
        end_time = perf_counter()
        logger.success("{} shutdown {} run_time:{}", user, func.__name__, end_time - start_time)
        return ret

    return wrapper
