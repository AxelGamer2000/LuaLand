from lupa.lua55 import LuaRuntime
from pathlib import Path
import json

class GameScriptingEngine:
    def __init__(self):
        self.lua = LuaRuntime()

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

    def execute_file(self, path:Path):
        self.lua.execute(path.read_text(encoding="utf-8"))

    def register(self, name:str, function):
        setattr(self.lua.globals(), name, function)

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
