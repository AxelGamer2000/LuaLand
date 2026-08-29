import luait

class Api:
    def __init__(self, script_engine:luait.GameScriptingEngine, display_script_engine:luait.GameScriptingDisplayEngine):
        self.script_engine = script_engine
        self.display_script_engine = display_script_engine

    def init(self):
        pass
