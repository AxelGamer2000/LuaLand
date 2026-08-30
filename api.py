from pathlib import Path
import json
import luait
import pygame

class Api:
    def __init__(self, script_engine:luait.GameScriptingEngine, display_script_engine:luait.GameScriptingDisplayEngine, screen:pygame.surface.Surface):
        self.script_engine = script_engine
        self.display_script_engine = display_script_engine
        self.screen = screen

    def init(self):
        self.script_engine.init()

        order_file = Path("modules/order.json")
        order_json = json.loads(order_file.read_text(encoding="utf-8"))
        order: list[str] = order_json["order"]
        order_path: list[Path] = [Path(path) for path in order]

        for module in order_path:
            print(f"{module.name} loaded")
            self.script_engine.execute_file(module)