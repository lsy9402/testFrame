from collections import namedtuple

from db.test_tools import tools_map, checks_map

TOOL = namedtuple("TOOL", ["module", "func"])
CHECK = namedtuple("CHECK", ["module", "func", "get_data"])


def add_tool(name=None):
    if callable(name):
        return add_tool()(name)

    def wrapper(func):
        nonlocal name
        name = name or func.__name__
        tools_map[name] = TOOL(module=func.__module__, func=func.__name__)
        return func

    return wrapper


def add_check(name=None):
    if callable(name):
        return add_check()(name)

    def wrapper(func):
        nonlocal name
        name = name or func.__name__
        checks_map[name] = CHECK(module=func.__module__, func=func.__name__, get_data=None)

        def get_data(get_data_func):
            checks_map[name] = CHECK(module=func.__module__, func=func.__name__, get_data=get_data_func.__name__)
            return get_data_func

        setattr(func, "get_data", get_data)
        return func

    return wrapper
