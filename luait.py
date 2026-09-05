from lupa.lua55 import LuaRuntime
from pathlib import Path
from loguru import logger
from typing import Callable
import json
import api

class Module:
    def __init__(self, path:Path, api_function:Callable):
        self.path: Path = path
        self.module_name: str = path.name
        self.lua: LuaRuntime = LuaRuntime()

        api_function(self.lua, self.module_name)

        self.start_function: Callable = None
        self.render_function: Callable = None
        self.update_function: Callable = None

        env = self.lua.table()
        env.module_name = self.module_name

        self.lua.globals()._env = env

    def execute(self):
        self.lua.execute(self.path.read_text(encoding="utf-8"))

        self.start_function = self.lua.globals().start
        self.render_function = self.lua.globals().render
        self.update_function = self.lua.globals().update

    def remove_functions(self, functions_list:list):
        for function in functions_list:
            self.lua.globals()[function] = None

    def start(self):
        if self.start_function is not None:
            self.start_function()

    def render(self):
        if self.render_function is not None:
            self.render_function()

    def update(self):
        if self.update_function is not None:
            self.update_function()


class GameScriptingEngine:
    def __init__(self):
        self.logger = logger.bind(thread="lua", source="GameScriptingEngine")

        self.modules_order_file: Path = None
        self.modules_dir: Path = None

    def init(self):
        self.modules_dir = Path("modules")
        self.modules_dir.mkdir(exist_ok=True)

        self.modules_order_file = Path("modules/order.json")
        self.modules_order_file.touch(exist_ok=True)

        if self.modules_order_file.read_text().strip() == "":
            default_json = {"order": []}
            self.modules_order_file.write_text(json.dumps(default_json, indent=2))

    def expose_api(self, modding_api:api.ModdingApi, lua:LuaRuntime):
        if modding_api.is_table:
            table = lua.table()
            for function_name in modding_api.get_api_functions():
                table[function_name.replace("api_", "")] = getattr(modding_api, function_name)

            setattr(lua.globals(), modding_api.name, table)
        else:
            for function_name in modding_api.get_api_functions():
                setattr(lua.globals(), function_name.replace("api_", ""), getattr(modding_api, function_name))

class DisplayFunction:
    def __init__(self, name:str, args:list):
        self.name:str = name
        self.args:list = args

class GameScriptingDisplayEngine:
    def __init__(self):
        self.binding_display_functions_table:dict = {}
        self.display_functions:list[DisplayFunction] = []

    def add_binding_function(self, function_name:str, function):
        self.binding_display_functions_table[function_name] = function

    def add_function(self, function_name:str, args:list):
        self.display_functions.append(DisplayFunction(function_name, args))

    def update(self):
        for display_function in self.display_functions:
            self.binding_display_functions_table[display_function.name](*display_function.args)
