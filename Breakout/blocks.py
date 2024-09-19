import pygame
class Brick:
    def __init__(self, color, width, height, x, y):
        self.Surface = pygame.Surface([width, height])
        self.Surface.fill(color)
        self.Rect = self.Surface.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.Surface, self.Rect)
