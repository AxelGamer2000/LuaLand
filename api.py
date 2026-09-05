from pathlib import Path
from lupa.lua55 import LuaRuntime
import json
import luait
import pygame
from loguru import logger

class ModdingApi:
    def __init__(self, is_table:bool, name:str = "", display_script_engine:luait.GameScriptingDisplayEngine = None):
        self.is_table = is_table
        self.name = name
        self.display_script_engine = display_script_engine

    def get_api_functions(self):
        functions = [
            getattr(self, name) for name in dir(self) if callable(getattr(self, name)) and not name.startswith("_")
        ]
        function_names: list[str] = [func.__name__ for func in functions]
        functions_api_names: list[str] = [func for func in function_names if func.startswith("api_")]

        return functions_api_names

    def get_display_api_functions(self):
        functions = [
            getattr(self, name) for name in dir(self) if callable(getattr(self, name)) and not name.startswith("_")
        ]
        function_names: list[str] = [func.__name__ for func in functions]
        functions_api_names: list[str] = [func for func in function_names if func.startswith("display_api_")]

        return functions_api_names

class Api:
    def __init__(self, script_engine:luait.GameScriptingEngine, display_script_engine:luait.GameScriptingDisplayEngine, screen:pygame.surface.Surface):
        self.script_engine = script_engine
        self.display_script_engine = display_script_engine
        self.screen = screen

        self.order_file = Path("modules/order.json")
        self.order_json = json.loads(self.order_file.read_text(encoding="utf-8"))
        self.order: list[str] = self.order_json["order"]
        self.order_path: list[Path] = [Path(path) for path in self.order]
        self.modules: list[luait.Module] = []

        self.start_module: list = []
        self.update_module: list = []
        self.render_module: list = []

    def init(self):
        self.script_engine.init()

        for module_path in self.order_path:
            self.modules.append(luait.Module(module_path, self.register_api))

        for module in self.modules:
            self.script_engine.logger.info(f"{module.module_name} loaded")
            module.remove_functions(["require", "dofile", "loadfile", "print"])
            module.execute()

    def register_api(self, lua:LuaRuntime, module_name:str):
        self.script_engine.expose_api(BaseApi(), lua)
        self.script_engine.expose_api(ConsoleApi(module_name), lua)

    def start_event(self):
        for module in self.modules:
            module.start()

    def update_event(self):
        for module in self.modules:
            module.update()

    def render_event(self):
        for module in self.modules:
            module.render()

# Modding Api

class BaseApi(ModdingApi):
    def __init__(self):
        super().__init__(False)


class ConsoleApi(ModdingApi):
    def __init__(self, module_name:str):
        super().__init__(True, "console")
        self.module_name = module_name
        self.console_log = logger.bind(thread="lua", source=self.module_name)

    def api_info(self, message):
        self.console_log.info(message)

    def api_warn(self, message):
        self.console_log.warning(message)

    def api_err(self, message):
        self.console_log.error(message)
