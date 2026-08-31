from pathlib import Path
import json
import luait
import pygame

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

        for module in self.order_path:
            print(f"{module.name} loaded")
            self.script_engine.execute_file(module)

            self.start_module.append(self.script_engine.lua.globals().start)
            self.update_module.append(self.script_engine.lua.globals().update)
            self.render_module.append(self.script_engine.lua.globals().render)

        self.register_functions()

    def register_functions(self):
        pass

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

