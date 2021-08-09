from importlib import import_module

from aioredis import Redis
from fastapi import APIRouter, Request, Query, Depends
from jsonpath import jsonpath

from core.config import settings
from db.base import execute, get_redis
from db.test_tools import tools_map, checks_map
from schemas.public import Public_X1, Public_Y1, Public_Z1, Res
from utils.HttpUtil import send_post

public_router = APIRouter(tags=["公共方法"])


@public_router.post("/public", name="公共接口", response_model=Public_Z1)
async def public_api(input_data: Public_X1,
                     req: Request,
                     env: settings.ENV = Query(None),
                     redis: Redis = Depends(get_redis)) -> Public_Z1:
    data = await build_public(env, input_data, req)
    await data(redis)
    output = await build_output(data)
    await save_log(input_data, data, output)
    return output


def get_info(info) -> (str, dict):
    if isinstance(info, str):
        return info, {}
    elif isinstance(info, dict):
        for k, v in info.items():
            return k, v
    else:
        raise Exception


class Public(Public_Y1):
    def run_tools(self):
        tools_info = []
        for tool in self.tools:
            tool_name, tool_args = get_info(tool)
            _tool = tools_map.get(tool_name)
            tools_info.append(getattr(import_module(_tool.module), _tool.func)(**tool_args))
        self.tools = tools_info

    def checks_get_data(self, post) -> list:
        checks_info = []
        for check in self.checks:
            check_name, check_args = get_info(check)
            _check = checks_map.get(check_name)
            if _check.get_data:
                checks_info.append(getattr(import_module(_check.module), _check.get_data)(**check_args))
            else:
                checks_info.append(None)
        return checks_info

    def load_data(self, post: Res):
        def _load(data: object) -> object:
            if isinstance(data, dict):
                for k, v in data.items():
                    data[k] = _load(v)
            elif isinstance(data, list):
                for item in data:
                    _load(item)
            elif isinstance(data, str) and data.startswith("$"):
                ret = jsonpath(self.tools, data)
                return (ret and ret[0]) or data
            else:
                return data

        _load(post.data)

    def run_check(self, checks_info) -> bool:
        return True

    async def __call__(self, redis: Redis):
        self.run_tools()
        checks_info = []
        for post in self.posts:
            checks_info.append(self.checks_get_data(post))
            self.load_data(post)
            post.status, post.res = await send_post(post.url, post.data, headers=post.headers)
        self.result = self.run_check(checks_info)


async def build_public(env: settings.ENV, input_data: Public_X1, req: Request) -> Public:
    return Public(env=env or settings.ENV._member_map_[settings.ENV._member_names_[0]],
                  user=req.client.host,
                  **input_data.copy(deep=True).dict())


async def build_output(data: Public) -> Public_Z1:
    return Public_Z1(**data.dict())


async def save_log(input_data: Public_X1, data: Public_Y1, output: Public_Z1):
    return await execute("insert_log", {"user": data.user, "req": input_data.json(), "res": output.json()})
