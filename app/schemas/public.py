from typing import Union, List

from pydantic import BaseModel, AnyHttpUrl, Field, validator

from core.config import settings


class Post(BaseModel):
    url: Union[AnyHttpUrl, dict, str] = Field(..., title="请求路径")
    data: dict = Field(..., title="请求数据")

    class Config:
        title = "测试接口信息"
        schema_extra = {
            "example": {
                "url": "http://127.0.0.1:8000/test",
                "data": {"test": "test"}
            }
        }


class Res(BaseModel):
    url: AnyHttpUrl = Field(..., title="请求路径")
    data: dict = Field(..., title="请求数据")
    status: int = Field(None, title="返回状态码")
    res: dict = Field(None, title="返回数据")


class Public_X1(BaseModel):
    posts: List[Post]

    class Config:
        title = "公共接口输入"


class Public_Z1(BaseModel):
    env: settings.ENV
    posts: List[Res]

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
