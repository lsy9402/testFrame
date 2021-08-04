from fastapi import APIRouter, Request, Query

from core.config import settings
from db.base import execute
from schemas.public import Public_X1, Public_Y1, Public_Z1
from utils.HttpUtil import send_post
from utils.LogUtil import add_log

public_router = APIRouter(tags=["公共方法"])


@public_router.post("/public", name="公共接口", response_model=Public_Z1)
@add_log
async def public_api(input_data: Public_X1,
                     req: Request,
                     env: settings.ENV = Query(None)) -> Public_Z1:
    data = await build_public(env, input_data, req)
    await run_test(data)
    output = await build_output(data)
    await save_log(input_data, data, output)
    return output


async def build_public(env: settings.ENV, input_data: Public_X1, req: Request) -> Public_Y1:
    return Public_Y1(env=env or settings.ENV._member_map_[settings.ENV._member_names_[0]],
                     user=req.client.host,
                     **input_data.copy(deep=True).dict())


async def run_test(data: Public_Y1):
    for post in data.posts:
        post.status, post.res = await send_post(post.url, post.data)
    return data


async def build_output(data: Public_Y1) -> Public_Z1:
    return Public_Z1(**data.dict())


async def save_log(input_data: Public_X1, data: Public_Y1, output: Public_Z1):
    return await execute("insert_log", {"user": data.user, "req": input_data.json(), "res": output.json()})
