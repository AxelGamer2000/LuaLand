import pygame
import luait

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.script_engine = luait.GameScriptingEngine()
        self.display_script_engine = luait.GameScriptingDisplayEngine()

    def run(self):
        pygame.init()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill("#7d94b5")

            self.display_script_engine.update()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()