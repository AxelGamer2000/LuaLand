import pygame
import luait
from api import Api
from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format="<level>[{time:HH:mm:ss}] [{extra[thread]}/{level}] [{extra[source]}]: {message}</level>",
    colorize=True
)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

script_engine = luait.GameScriptingEngine()
game_data = luait.GameData()
api = Api(script_engine, game_data, screen)

running = True
start_event = True

api.init()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if start_event:
        api.start_event()
        start_event = False

    screen.fill(game_data.background_color)

    api.update_event()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
