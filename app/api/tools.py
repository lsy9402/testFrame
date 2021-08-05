from fastapi import APIRouter

from db.test_tools import tools_map, checks_map

tools_router = APIRouter(tags=["工具集"])


@tools_router.get("/get_tools", name="获取工具集信息")
def get_tools():
    return tools_map


@tools_router.get("/get_checks", name="获取检查脚本集信息")
def get_checks():
    return checks_map
