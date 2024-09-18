
import sys
import pygame
from pygame.locals import *

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
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

def main_menu():
    lateral_bar = pygame.Surface((20, 1000))
    top_bar = pygame.Surface((720, 40))

    lateral_bar.fill(COLOR_WHITE)
    top_bar.fill(COLOR_WHITE)

    top_rect = top_bar.get_rect(topleft=(0, 0))
    left_rect = lateral_bar.get_rect(topleft=(0, 0))
    right_rect = lateral_bar.get_rect(topright=(720, 0))

    screen.blit(lateral_bar, right_rect)
    screen.blit(lateral_bar, left_rect)
    screen.blit(top_bar, top_rect)


# Game loop
while game_loop:

    # Get inputs here
    for event in pygame.event.get():
        if event.type == QUIT:
            game_loop = False

    # Main game here

    # Load objects of the game here
    screen.fill(COLOR_BLACK)
    main_menu()
    pygame.display.update()
    pygame.display.flip()
    fpsClock.tick(fps)

pygame.quit()
sys.exit()



# Mensagem de alteração Teste
