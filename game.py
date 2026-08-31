import pygame
import luait
from api import Api

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

script_engine = luait.GameScriptingEngine()
display_script_engine = luait.GameScriptingDisplayEngine()
api = Api(script_engine, display_script_engine, screen)

running = True
start_event = True

api.init()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if start_event:
        api.start_event()
        api.render_event()
        start_event = False

    screen.fill("#7d94b5")

    api.update_event()

    display_script_engine.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
