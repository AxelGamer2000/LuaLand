from lupa.lua55 import LuaRuntime
from pathlib import Path
from loguru import logger
import json
import api

class GameScriptingEngine:
    def __init__(self):
        self.lua = LuaRuntime()
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

    def execute(self, code:str):
        self.lua.execute(code)

    def execute_file(self, path:Path, name):
        self.lua.execute(f"_name = '{name}'\n{path.read_text(encoding="utf-8")}")

    def expose_api(self, modding_api:api.ModdingApi):
        if modding_api.is_table:
            table = self.lua.table()
            for function_name in modding_api.get_api_functions():
                table[function_name.replace("api_", "")] = getattr(modding_api, function_name)

            setattr(self.lua.globals(), modding_api.name, table)
        else:
            for function_name in modding_api.get_api_functions():
                setattr(self.lua.globals(), function_name.replace("api_", ""), getattr(modding_api, function_name))

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
