import pygame

class Brick():
    def __init__(self, color, width, height):
        super().__init__()

        self.Surface = pygame.Surface([width, height])
        self.Surface.fill(color)
        self.Rect = self.Surface.get_rect()
