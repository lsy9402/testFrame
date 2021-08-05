from core.tools import add_tool


@add_tool(name="测试工具")
def test_tool(*args, **kwargs):
    pass


@add_tool(name="获取用户")
def get_user(*args, **kwargs):
    return {
        "username": "test",
        "password": "test",
        "token": "test_token",
        "email": "test@email.com"
    }


@add_tool(name="获取用户密码")
def get_user(username, *args, **kwargs):
    table = {
        "test": {
            "username": "test",
            "password": "test",
            "token": "test_token",
            "email": "test@email.com"
        }
    }
    return table.get(username)
