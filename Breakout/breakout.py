
import sys
import pygame
from pygame.locals import *

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 128, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (121, 182, 201)

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()

width = 720
height = 1000
screen = pygame.display.set_mode((width, height))
game_loop = True

# Game loop
while game_loop:

    # Get inputs here
    for event in pygame.event.get():
        if event.type == QUIT:
            game_loop = False

    # Main game here

    # Load objects of the game here
    screen.fill(COLOR_BLACK)
    pygame.display.update()
    pygame.display.flip()
    fpsClock.tick(fps)

pygame.quit()
sys.exit()
