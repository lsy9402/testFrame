from aioredis import create_redis_pool, Redis
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, String, JSON, TIMESTAMP

from core.config import settings, database_driven

__all__ = ["db", "fetch_all", "db_init", "execute", "get_redis", "close_redis"]

# 数据库类型://用户名:密码@IP地址:端口号/数据库名
db = Database(f"{settings.DB_TYPE}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


async def fetch_all(name, values=None):
    return await db.fetch_all(settings.SQL.get(name), values)


async def execute(name, values=None):
    return await db.execute(settings.SQL.get(name), values)


def db_init():
    metadata = MetaData()
    # 数据库类型+数据库驱动名称://用户名:密码@IP地址:端口号/数据库名
    engine = create_engine(f"{settings.DB_TYPE}+{database_driven[settings.DB_TYPE]}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    Table("log", metadata,
          Column("user", String(30), comment="用户"),
          Column("req", JSON, comment="请求"),
          Column("res", JSON, comment="响应"),
          Column("time", TIMESTAMP, comment="时间"),
          comment="日志表"
          )
    metadata.create_all(engine)


redis: Redis = None


async def get_redis():
    global redis
    if redis is None:
        redis = await create_redis_pool(address=(settings.DB_HOST, settings.REDIS_PORT))
    return redis


async def close_redis():
    global redis
    if redis:
        await redis.save()
        redis.close()
        await redis.wait_closed()
