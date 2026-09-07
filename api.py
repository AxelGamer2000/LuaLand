from pathlib import Path
from lupa.lua55 import LuaRuntime
import json
import luait
import pygame
from loguru import logger

class ModdingApi:
    def __init__(self, is_table:bool, name:str = ""):
        self.is_table = is_table
        self.name = name

    def get_api_functions(self):
        functions = [
            getattr(self, name) for name in dir(self) if callable(getattr(self, name)) and not name.startswith("_")
        ]
        function_names: list[str] = [func.__name__ for func in functions]
        functions_api_names: list[str] = [func for func in function_names if func.startswith("api_")]

        return functions_api_names

class Api:
    def __init__(self, script_engine:luait.GameScriptingEngine, game_data:luait.GameData, screen:pygame.surface.Surface):
        self.script_engine = script_engine
        self.game_data = game_data
        self.screen = screen

        self.order_file = Path("modules/order.json")
        self.order_json = json.loads(self.order_file.read_text(encoding="utf-8"))
        self.order: list[str] = self.order_json["order"]
        self.order_path: list[Path] = [Path(path) for path in self.order]
        self.modules: list[luait.Module] = []

        self.start_module: list = []
        self.update_module: list = []

    def init(self):
        self.script_engine.init()

        for module_path in self.order_path:
            self.modules.append(luait.Module(module_path, self.register_api))

        for module in self.modules:
            self.script_engine.logger.info(f"{module.module_name} loaded")
            module.remove_functions(["require", "dofile", "loadfile", "print"])
            module.execute()

    def register_api(self, lua:LuaRuntime, module_name:str):
        self.script_engine.expose_api(BaseApi(self.game_data), lua)
        self.script_engine.expose_api(ConsoleApi(module_name), lua)
        self.script_engine.expose_api(ScreenApi(self.screen, self.game_data), lua)

    def start_event(self):
        for module in self.modules:
            module.start()

    def update_event(self):
        for module in self.modules:
            module.update()

# Modding Api

class BaseApi(ModdingApi):
    def __init__(self, game_data:luait.GameData):
        self.game_data = game_data
        super().__init__(False)

    def api_get_title(self):
        return self.game_data.title

    def api_set_title(self, new_title):
        self.game_data.title = new_title


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

class ScreenApi(ModdingApi):
    def __init__(self, screen:pygame.surface.Surface, game_data:luait.GameData):
        super().__init__(True, "screen")
        self.screen = screen
        self.game_data = game_data

    def api_set_background_color(self, color):
        self.game_data.background_color = color

    def api_get_background_color(self):
        return self.game_data.background_color

    def api_rectangle(self, x, y, color, width, height):
        pygame.draw.rect(self.screen, color, [x, y, width, height])