import pygame

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        vector = pygame.Vector2(self.x, self.y).normalize()
        return Vector2(vector.x, vector.y)

