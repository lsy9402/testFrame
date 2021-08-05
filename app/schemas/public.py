from typing import Union, List, Optional

from pydantic import BaseModel, AnyHttpUrl, Field, validator

from core.config import settings
from db.test_tools import tools_map, checks_map


class Post(BaseModel):
    url: Union[AnyHttpUrl, dict, str] = Field(..., title="请求路径")
    headers: dict = Field(None, title="请求头信息")
    data: dict = Field(..., title="请求数据")

    class Config:
        title = "测试接口信息"
        schema_extra = {
            "example": {
                "url": "http://127.0.0.1:8000/login",
                "data": {
                    "username": "test",
                    "password": "test"
                }
            }
        }


class Res(BaseModel):
    url: AnyHttpUrl = Field(..., title="请求路径")
    headers: Optional[dict] = Field(None, title="请求头信息")
    data: dict = Field(..., title="请求数据")
    status: int = Field(None, title="返回状态码")
    res: dict = Field(None, title="返回数据")

    class Config:
        title = "测试接口响应信息"


class Public_X1(BaseModel):
    posts: List[Post] = Field([], title="测试接口")
    tools: list = Field([], title="测试工具集")

    @validator("tools")
    def validate_tools(cls, tools):
        for tool in tools:
            if isinstance(tool, str):
                tool_name = tool
            elif isinstance(tool, dict):
                tool_name = list(tool)[0]
            else:
                raise ValueError(f"插件{tool}异常")
            if tool_name in tools_map:
                return tools
            else:
                raise ValueError(f"插件{tool_name}不存在")
        return tools

    checks: list = Field([], title="检查脚本集")

    @validator("checks")
    def validate_checks(cls, checks):
        for check in checks:
            if check not in checks_map:
                raise ValueError(f"检查脚本{check}不存在")
        return checks

    class Config:
        title = "公共接口输入"


class Public_Z1(BaseModel):
    env: settings.ENV
    posts: List[Res]
    tools: list
    checks: list
    result: bool = False

    class Config:
        title = "公共接口输出"


class Public_Y1(Public_Z1):
    user: str = Field(..., title="用户IP")

    @validator("user", pre=True)
    def validate_user(cls, value):
        if value == "127.0.0.1":
            value = settings.LOCALHOST
        return value

    class Config:
        title = "公共接口内部数据"
