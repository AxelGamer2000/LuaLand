import pygame
import luait

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

script_engine = luait.GameScriptingEngine(luait.lua)
display_script_engine = luait.GameScriptingDisplayEngine()

display_script_engine.add_binding_function("fill", screen.fill)
display_script_engine.add_function("fill", ["#7d94b5"])

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #screen.fill("#7d94b5")

    display_script_engine.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
