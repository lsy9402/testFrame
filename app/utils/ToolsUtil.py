from importlib import import_module
from pathlib import Path


def get_module_name(file: Path, name=None):
    if file.parent.name == "app":
        return file.name + "." + name
    else:
        return get_module_name(file.parent, name=file.name.rstrip(".py") if name is None else file.name + "." + name)


def load_test_module():
    tools_dir = Path.cwd().joinpath("testTools")

    def _load_module(py_dir):
        for file in py_dir.rglob("*.py"):
            if file.name != "__init__.py":
                import_module(get_module_name(file))

    _load_module(tools_dir)
