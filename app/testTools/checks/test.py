from core.tools import add_check


@add_check(name="测试检查脚本")
def test_check():
    pass


@test_check.get_data
def get_data():
    pass
