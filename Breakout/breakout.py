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

LIST_COLORS = [COLOR_RED, COLOR_ORANGE, COLOR_GREEN, COLOR_YELLOW]

red_bricks = []
orange_bricks = []
green_bricks = []
yellow_bricks = []

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

start = False

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


def create_scenario():
    lateral_bar = pygame.Surface((20, 1000))
    bottom_bar = pygame.Surface((720, 20))
    top_bar = pygame.Surface((720, 40))
    white_bar = pygame.Surface((15, 80))
    blocks = pygame.Surface((20, 70))

    white_bar.fill(COLOR_WHITE)
    lateral_bar.fill(COLOR_WHITE)
    top_bar.fill(COLOR_WHITE)
    bottom_bar.fill(COLOR_BLUE)

    top_rect = top_bar.get_rect(topleft=(0, 0))
    left_rect = lateral_bar.get_rect(topleft=(0, 0))
    right_rect = lateral_bar.get_rect(topright=(720, 0))
    bottom_rect = bottom_bar.get_rect(topleft=(0, 880))

    screen.blit(lateral_bar, right_rect)
    screen.blit(lateral_bar, left_rect)
    screen.blit(top_bar, top_rect)
    screen.blit(bottom_bar, bottom_rect)

    score_font = pygame.font.Font('assets/pong-score.ttf', 60)
    score_text = score_font.render(score_txt, False, COLOR_WHITE)
    try_text = score_font.render(try_txt, False, COLOR_WHITE)

    for i in range(len(LIST_COLORS)):
        blocks.fill(LIST_COLORS[i])
        screen.blit(blocks, (0, 195 + 60 * i))
        screen.blit(blocks, (700, 195 + 60 * i))

    blocks.fill(COLOR_BLUE)
    screen.blit(blocks, (0, 865))
    screen.blit(blocks, (700, 865))

    screen.blit(try_text, (400, 50))
    screen.blit(score_text, (100, 130))
    screen.blit(white_bar, (50, 40))


def create_bricks():
    for color_index, color in enumerate(LIST_COLORS):
        for fila in range(2):
            for pos in range(13):
                x = 20 + 52.9 * pos
                y = 200 + (color_index * 60) + (fila * 30)  # Adjust y position based on color
                block = blocks.Brick(color, 45, 20, x, y)
                if color == COLOR_RED:
                    red_bricks.append(block)
                elif color == COLOR_ORANGE:
                    orange_bricks.append(block)
                elif color == COLOR_GREEN:
                    green_bricks.append(block)
                elif color == COLOR_YELLOW:
                    yellow_bricks.append(block)
    for brick in red_bricks + orange_bricks + green_bricks + yellow_bricks:
        brick.draw(screen)


def main_menu():
    show_text = True
    text_font = pygame.font.Font('assets/ARCADE_I.TTF', 20)
    start_text = text_font.render('Press SPACE to start the game', False, COLOR_WHITE)

    if pygame.time.get_ticks() % 1000 <= 100:
        show_text = not show_text
    if show_text:
        screen.blit(start_text, (75, 700))


# Game loop
while game_loop:
    # Get inputs here
    for event in pygame.event.get():
        if event.type == QUIT:
            game_loop = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print('Jogo deve iniciar!!!')
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

    # Main game here
    screen.fill(COLOR_BLACK)
    create_scenario()
    create_bricks()
    main_menu()

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
