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
breakout = True
menu_loop = True
game_loop = False

score_txt = '000'
try_txt = '0'

# player
paddle_speed = 10
paddle_height = 25
paddle_width = 100
paddle_x = width // 2 - paddle_width // 2
paddle_y = height - 120
paddle_move_right = False
paddle_move_left = False
paddle_hit_count = 0

# Draw Ball
ball_size = 10
ball_x = width // 2 - ball_size // 2
ball_y = height // 2 - ball_size // 2
ball_dx = 5
ball_dy = 5

# Sound effects
hit_brick = pygame.mixer.Sound('assets/brick.wav')
hit_paddle = pygame.mixer.Sound('assets/paddle.wav')
hit_wall = pygame.mixer.Sound('assets/wall.wav')


def score_display(point, score_txt):
    score_txt = str(int(score_txt) + point)
    if len(score_txt) == 1:
        score_txt = '00'+score_txt
    elif len(score_txt) == 2:
        score_txt = '0'+score_txt

    return score_txt


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
    if not game_loop:
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

    return bottom_bar, bottom_rect


def create_bricks():
    for color_index, color in enumerate(LIST_COLORS):
        for fila in range(2):
            for pos in range(14):
                x = 20 + 48.9 * pos
                y = 200 + (color_index * 60) + (fila * 30)  # Adjust y position based on color
                block = blocks.Brick(color, 44, 20, x, y)
                if color == COLOR_RED:
                    red_bricks.append(block)
                elif color == COLOR_ORANGE:
                    orange_bricks.append(block)
                elif color == COLOR_GREEN:
                    green_bricks.append(block)
                elif color == COLOR_YELLOW:
                    yellow_bricks.append(block)


def main_menu():
    show_text = True
    text_font = pygame.font.Font('assets/ARCADE_I.TTF', 20)
    start_text = text_font.render('Press SPACE to start the game', False, COLOR_WHITE)

    if pygame.time.get_ticks() % 1000 <= 100:
        show_text = not show_text
    if show_text:
        screen.blit(start_text, (75, 700))


# Create blocks once
create_bricks()

collision = False


def brick_collision(ball, brick_list):
    global collision
    if not collision:
        for brick in brick_list[:]:
            if ball.colliderect(brick.Rect) and ball_dy < 0:
                brick_list.remove(brick)
                hit_brick.play()
                collision = True
                return True
    return False


while breakout:
    # Game loop
    while menu_loop:
        # Get inputs here
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print('Jogo deve iniciar!!!')
                game_loop = True
                menu_loop = False

        # Move Ball + rest paddle hit count
        ball_x += ball_dx
        ball_y += ball_dy
        paddle_hit_count = 0

        # Main game here
        screen.fill(COLOR_BLACK)
        bottom_bar, bottom_rect = create_scenario()
        main_menu()

        # Draw bricks + ball
        for brick in red_bricks + orange_bricks + green_bricks + yellow_bricks:
            brick.draw(screen)
        ball = pygame.draw.rect(screen, COLOR_WHITE, (ball_x, ball_y, ball_size, ball_size))

        # Detect collision
        if ball_x <= 15 or ball_x + ball_size >= width:  # Left
            ball_dx = -ball_dx
            hit_wall.play()
        if ball_y <= 35 or ball_y + ball_size >= height:  # Top
            ball_dy = -ball_dy
            hit_wall.play()
        if ball_x >= 680 or ball_x + ball_size >= width:  # Right
            ball_dx = -ball_dx
            hit_wall.play()
        if ball.colliderect(bottom_rect) and ball_dy > 0:  # Bottom rect
            ball_dy = -ball_dy
            collision = False
            hit_wall.play()
        for brick in red_bricks + orange_bricks + green_bricks + yellow_bricks:  # Bricks
            if ball.colliderect(brick.Rect) and ball_dy < 0:
                ball_dy = -ball_dy
                hit_brick.play()

        # Load objects of the game here
        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)

    while game_loop:
        # Get inputs here
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
            paddle_x += paddle_speed

        # Move Ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Main game here
        screen.fill(COLOR_BLACK)
        bottom_bar, bottom_rect = create_scenario()

        # Draw bricks + ball + player
        for brick in red_bricks + orange_bricks + green_bricks + yellow_bricks:
            brick.draw(screen)
        ball = pygame.draw.rect(screen, COLOR_WHITE, (ball_x, ball_y, ball_size, ball_size))
        paddle = pygame.draw.rect(screen, COLOR_BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

        # Detect collision
        if ball_x <= 15 or ball_x + ball_size >= width:  # Left
            ball_dx = -ball_dx
            hit_wall.play()
        if ball_y <= 35:  # Top
            ball_dy = -ball_dy
            hit_wall.play()
        if ball_x >= 680 or ball_x + ball_size >= width:  # Right
            ball_dx = -ball_dx
            hit_wall.play()
        if ball.colliderect(paddle) and ball_dy > 0:  # Paddle
            ball_dy = -ball_dy
            # Ball Speed increase when u hit paddle 4 and 12 times
            paddle_hit_count = paddle_hit_count + 1
            if paddle_hit_count == 4:
                ball_dy *= -1.5
            if paddle_hit_count == 12:
                ball_dy *= -1.8
            hit_paddle.play()
            collision = False
        for brick_list in [red_bricks]:  # Brick
            if brick_collision(ball, brick_list):
                ball_dy *= -2
                points = 7
                score_txt = score_display(points, score_txt)
                hit_brick.play()
                break
        for brick_list in [orange_bricks]:  # Brick
            if brick_collision(ball, brick_list):
                ball_dy *= -1.5
                points = 5
                score_txt = score_display(points, score_txt)
                hit_brick.play()
                break
        for brick_list in [green_bricks]:  # Brick
            if brick_collision(ball, brick_list):
                ball_dy = -ball_dy
                points = 3
                score_txt = score_display(points, score_txt)
                hit_brick.play()
                break
        for brick_list in [yellow_bricks]:  # Brick
            if brick_collision(ball, brick_list):
                ball_dy = -ball_dy
                points = 1
                score_txt = score_display(points, score_txt)
                hit_brick.play()
                break

        if ball_y + ball_size >= height+10:
            try_txt = str(int(try_txt)+1)
            ball_x = width // 2 - ball_size // 2
            ball_y = height // 2 - ball_size // 2
            ball_dx = 5
            ball_dy = 5
            paddle_hit_count = 0

            if int(try_txt) == 3:
                menu_loop = True
                game_loop = False

        # Load objects of the game here
        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)

pygame.quit()
sys.exit()
