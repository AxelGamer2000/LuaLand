from pathlib import Path
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

        self.start_module: list = []
        self.update_module: list = []
        self.render_module: list = []

    def init(self):
        self.script_engine.init()
        self.register_api()

        #self.script_engine.lua.globals().print = None
        self.script_engine.lua.globals().require = None
        self.script_engine.lua.globals().dofile = None
        self.script_engine.lua.globals().loadfile = None

        for module in self.order_path:
            env = self.script_engine.lua.table()
            env._name = module.name

            self.script_engine.logger.info(f"{module.name} loaded")
            self.script_engine.execute_file(module, module.name)

            self.start_module.append(self.script_engine.lua.globals().start)
            self.update_module.append(self.script_engine.lua.globals().update)
            self.render_module.append(self.script_engine.lua.globals().render)

    def register_api(self):
        self.script_engine.expose_api(BaseApi())
        self.script_engine.expose_api(ConsoleApi(self.script_engine))

    def start_event(self):
        for start in self.start_module:
            if start is not None:
                start()

    def update_event(self):
        for update in self.update_module:
            if update is not None:
                update()

    def render_event(self):
        for render in self.render_module:
            if render is not None:
                render()

# Modding Api

class BaseApi(ModdingApi):
    def __init__(self):
        super().__init__(False)

class ConsoleApi(ModdingApi):
    def __init__(self, script_engine:luait.GameScriptingEngine):
        super().__init__(True, "console")
        self.script_engine = script_engine

    def api_log(self, message):
        logger_log = logger.bind(thread="lua", source=self.script_engine.lua.globals()._name)
        logger_log.info(message)