from importlib import import_module

from fastapi import APIRouter, Request, Query

from core.config import settings
from db.base import execute
from db.test_tools import tools_map, checks_map
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


def get_info(info) -> (str, dict):
    if isinstance(info, str):
        return info, {}
    elif isinstance(info, dict):
        for k, v in info.items():
            return k, v
    else:
        raise Exception


def run_tools(tools: list) -> list:
    tools_info = []
    for tool in tools:
        tool_name, tool_args = get_info(tool)
        _tool = tools_map.get(tool_name)
        tools_info.append(getattr(import_module(_tool.module), _tool.func)(**tool_args))
    return tools_info


def checks_get_data(checks: list) -> list:
    checks_info = []
    for check in checks:
        check_name, check_args = get_info(check)
        _check = checks_map.get(check_name)
        if _check.get_data:
            checks_info.append(getattr(import_module(_check.module), _check.get_data)(**check_args))
        else:
            checks_info.append(None)
    return checks_info


def run_check(posts, checks_info, checks) -> bool:
    return True


async def run_test(data: Public_Y1) -> Public_Y1:
    data.tools = run_tools(data.tools)
    checks_info = []
    for post in data.posts:
        checks_info.append(checks_get_data(data.checks))
        post.status, post.res = await send_post(post.url, post.data, headers=post.headers)
    data.result = run_check(data.posts, checks_info, data.checks)
    return data


async def build_output(data: Public_Y1) -> Public_Z1:
    return Public_Z1(**data.dict())


async def save_log(input_data: Public_X1, data: Public_Y1, output: Public_Z1):
    return await execute("insert_log", {"user": data.user, "req": input_data.json(), "res": output.json()})
