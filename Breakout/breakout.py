import sys
import pygame
from pygame.locals import *
import blocks

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 184, 254)

COLOR_RED = (209, 13, 9)
COLOR_ORANGE = (253, 171, 4)
COLOR_GREEN = (3, 250, 61)
COLOR_YELLOW = (232, 253, 39)

LIST_COLORS = [
    COLOR_RED, COLOR_ORANGE,
    COLOR_GREEN, COLOR_YELLOW
]

pygame.init()

fps = 60

clock = pygame.time.Clock()

width = 720
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout Game")
game_loop = True

score_txt = '000'
try_txt = '0'

# player
paddle_speed = 6
paddle_height = 25
paddle_width = 100
paddle_x = width // 2 - paddle_width // 2
paddle_y = height - 130
paddle_move_right = False
paddle_move_left = False

# Draw Ball
ball_size = 15
ball_x = width // 2 - ball_size // 2
ball_y = height // 2 - ball_size // 2
ball_dx = 5
ball_dy = 5

exibir_texto = True


def main_menu(exibir_texto):
    lateral_bar = pygame.Surface((20, 1000))
    bottom_bar = pygame.Surface((720, 20))
    top_bar = pygame.Surface((720, 40))
    white_bar = pygame.Surface((15, 80))
    blocks = pygame.Surface((20, 50))
    position = 200

    white_bar.fill(COLOR_WHITE)
    lateral_bar.fill(COLOR_WHITE)
    top_bar.fill(COLOR_WHITE)
    # bottom_bar.fill(COLOR_BLUE)

    top_rect = top_bar.get_rect(topleft=(0, 0))
    left_rect = lateral_bar.get_rect(topleft=(0, 0))
    right_rect = lateral_bar.get_rect(topright=(720, 0))
    bottom_rect = bottom_bar.get_rect(topleft=(0, 880))

    score_font = pygame.font.Font('assets/pong-score.ttf', 60)
    text_font = pygame.font.Font('assets/ARCADE_I.TTF', 20)
    score_text = pygame.font.Font.render(score_font, score_txt, False,
                                         COLOR_WHITE, None)
    try_text = pygame.font.Font.render(score_font, try_txt, False,
                                       COLOR_WHITE, None)
    start_text = pygame.font.Font.render(text_font, 'Press SPACE to start the game', False,
                                         COLOR_WHITE, None)

    screen.blit(lateral_bar, right_rect)
    screen.blit(lateral_bar, left_rect)
    screen.blit(top_bar, top_rect)
    screen.blit(bottom_bar, bottom_rect)

    for i in range(len(LIST_COLORS)):
        blocks.fill(LIST_COLORS[i])
        screen.blit(blocks, (0, position + 50 * i))
        screen.blit(blocks, (700, position + 50 * i))

    blocks.fill(COLOR_BLUE)
    screen.blit(blocks, (0, 865))
    screen.blit(blocks, (700, 865))

    screen.blit(try_text, (400, 50))
    screen.blit(score_text, (100, 130))
    screen.blit(white_bar, (50, 40))

    if pygame.time.get_ticks() % 1000 <= 100:
        exibir_texto = not exibir_texto
    if exibir_texto:
        screen.blit(start_text, (75, 700))


# Game loop
while game_loop:

    # Get inputs here
    for event in pygame.event.get():
        if event.type == QUIT:
            game_loop = False

        # A movimentação precisa de ajustes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                paddle_move_right = True

            if event.key == pygame.K_LEFT:
                paddle_move_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                paddle_move_right = False

            if event.key == pygame.K_LEFT:
                paddle_move_left = False



            if paddle_move_right:
                paddle_x += paddle_speed
            else:
                paddle_x += 0

            if paddle_move_left:
                paddle_x -= paddle_speed
            else:
                paddle_x += 0

            if event.key == pygame.K_SPACE:
                print('Jogo deve iniciar!!!')
    # Move Ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Detect Collision
    if ball_x <= 15 or ball_x + ball_size >= width:
        ball_dx = -ball_dx
    if ball_y <= 35 or ball_y + ball_size >= height:
        ball_dy = -ball_dy

    if ball_x >= 680 or ball_x + ball_size >= width:
        ball_dx = -ball_dx
    if ball_y >= 980 or ball_y + ball_size >= height:
        ball_dy = -ball_dy

    screen.fill(COLOR_BLACK)

    # Main game here
    main_menu(exibir_texto)

    # Draw ball
    pygame.draw.rect(screen, COLOR_WHITE, (ball_x, ball_y, ball_size, ball_size))

    # Draw player paddle
    pygame.draw.rect(screen, COLOR_BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Load objects of the game here
    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()
