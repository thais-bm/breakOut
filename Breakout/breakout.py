import sys
import pygame
from pygame.locals import *
import blocks

# Setup pygame
pygame.init()
fps = 60
clock = pygame.time.Clock()
width = 720
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout Game")

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 184, 254)
COLOR_RED = (209, 13, 9)
COLOR_ORANGE = (253, 171, 4)
COLOR_GREEN = (3, 250, 61)
COLOR_YELLOW = (232, 253, 39)
LIST_COLORS = [COLOR_RED, COLOR_ORANGE, COLOR_GREEN, COLOR_YELLOW]

# Bricks
red_bricks = []
orange_bricks = []
green_bricks = []
yellow_bricks = []
brick_groups = []
collision = False

# Main loops
breakout = True
menu_loop = True
game_loop = False

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
top_hit = 0
MAX_SPEED = 10
reduce_paddle = True

# Scores + wins
score_txt = '000'
try_txt = '0'
win = 0

# Sound effects
hit_brick = pygame.mixer.Sound('assets/brick.wav')
hit_paddle = pygame.mixer.Sound('assets/paddle.wav')
hit_wall = pygame.mixer.Sound('assets/wall.wav')


def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, paddle_y, score_txt, lives, brick_groups
    ball_x = width // 2 - ball_size // 2
    ball_y = height // 2 - ball_size // 2
    ball_dx = 5
    ball_dy = 5
    paddle_x = width // 2 - paddle_width // 2
    paddle_y = height - 120

    # Limpando as listas
    yellow_bricks.clear()
    green_bricks.clear()
    orange_bricks.clear()
    red_bricks.clear()
    brick_groups.clear()

    brick_groups = create_bricks()


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

    return bottom_rect, top_rect, right_rect, left_rect


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
    brick_groups = [
        (red_bricks, -1.5, 7),
        (orange_bricks, -1.3, 5),
        (green_bricks, -1.0, 3),
        (yellow_bricks, -1.0, 1)
    ]

    return brick_groups


def main_menu():
    show_text = True
    text_font = pygame.font.Font('assets/ARCADE_I.TTF', 20)
    start_text = text_font.render('Press SPACE to start the game', False, COLOR_WHITE)

    if pygame.time.get_ticks() % 1000 <= 100:
        show_text = not show_text
    if show_text:
        screen.blit(start_text, (75, 700))


def brick_collision(ball, brick_list):
    global collision
    if not collision:
        for brick in brick_list[:]:
            if ball.colliderect(brick.Rect):
                brick_list.remove(brick)
                hit_brick.play()
                collision = True
                return True
    return False


# Create blocks once
brick_groups = create_bricks()


while breakout:
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
    top_hit = 0

    # Menu loop
    while menu_loop:
        # Get inputs here
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score_txt = '000'
                try_txt = '0'
                game_loop = True
                menu_loop = False

        # Move Ball + rest paddle hit count
        ball_x += ball_dx
        ball_y += ball_dy
        paddle_hit_count = 0

        # Main game here
        screen.fill(COLOR_BLACK)
        bottom_rect, top_rect, right_rect, left_rect = create_scenario()
        main_menu()

        # Draw bricks + ball
        for brick in red_bricks + orange_bricks + green_bricks + yellow_bricks:
            brick.draw(screen)
        ball = pygame.draw.rect(screen, COLOR_WHITE, (ball_x, ball_y, ball_size, ball_size))

        # Detect collision
        if ball_x <= 15 or ball_x + ball_size >= width:  # Left / Right
            ball_dx = -ball_dx
            hit_wall.play()
        if ball_y <= 35 or ball_y + ball_size >= height:  # Top
            ball_dy = -ball_dy
            hit_wall.play()
        if ball_x >= 680 or ball_x + ball_size >= width:  # Right
            ball_dx = -ball_dx
            hit_wall.play()
        if ball.colliderect(bottom_rect) and ball_dy > 0:  # Blue rect
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

    # Game loop
    while game_loop:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # paddle movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle_x > 0:
            paddle_x -= paddle_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle_x < width - paddle_width:
            paddle_x += paddle_speed

        # Move Ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Speed Limit (2 * inicial speed)
        ball_dx = max(-MAX_SPEED, min(MAX_SPEED, ball_dx))
        ball_dy = max(-MAX_SPEED, min(MAX_SPEED, ball_dy))

        # Main game here
        screen.fill(COLOR_BLACK)
        bottom_rect, top_rect, right_rect, left_rect = create_scenario()

        # Draw bricks + ball + player
        for brick in red_bricks + orange_bricks + green_bricks + yellow_bricks:
            brick.draw(screen)
        ball = pygame.draw.rect(screen, COLOR_WHITE, (ball_x, ball_y, ball_size, ball_size))
        paddle = pygame.draw.rect(screen, COLOR_BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

        # Detect collision
        if ball.colliderect(left_rect) and ball_dx < 0:  # Left
            ball_dx = -ball_dx
            collision = False
            hit_wall.play()
        if ball.colliderect(top_rect) and ball_dy < 0:  # Top
            ball_dy = -ball_dy
            if reduce_paddle:
                paddle_height = paddle_height // 2
                reduce_paddle = False
            collision = False
            hit_wall.play()
        if ball.colliderect(right_rect) and ball_dx > 0:  # Right
            ball_dx = -ball_dx
            collision = False
            hit_wall.play()
        if ball.colliderect(paddle) and ball_dy > 0:  # Paddle
            ball_dy = -ball_dy
            collision = False

        # Insert the angle adjustment code
            ball_position_on_paddle = (ball_x + ball_size / 2) - paddle_x
            paddle_middle = paddle_width / 2

            if ball_position_on_paddle < paddle_middle / 2:
                ball_dx = -abs(ball_dx) - 2
            elif ball_position_on_paddle < paddle_middle:
                ball_dx = -abs(ball_dx)
            elif ball_position_on_paddle < paddle_middle + paddle_middle / 2:
                ball_dx = abs(ball_dx)
            else:
                ball_dx = abs(ball_dx) + 2

            paddle_hit_count = paddle_hit_count + 1
            if paddle_hit_count == 4 or paddle_hit_count == 12:
                ball_dx *= 1.1
                ball_dy *= 1.1
            hit_paddle.play()
            collision = False

        # Collision detection for blocks
        for brick_list, speed_factor, points in brick_groups:
            if brick_collision(ball, brick_list):
                ball_dy *= speed_factor
                score_txt = score_display(points, score_txt)
                hit_brick.play()
                break

        # Ball misses
        if ball_y + ball_size >= height+10:
            try_txt = str(int(try_txt)+1)
            ball_x = width // 2 - ball_size // 2
            ball_y = height // 2 - ball_size // 2
            ball_dx = 5
            ball_dy = 5
            paddle_hit_count = 0

        # Condicao de derrota
            if int(try_txt) == 3:
                menu_loop = True
                game_loop = False

        # Condicao de vitoria: limpar os retangulos 2 vezes
        # -> jogo não tem tela de game over
        if len(red_bricks + orange_bricks + green_bricks + yellow_bricks) == 0:
            reset_game()
            win += 1
        
        if win == 2:
            print('Fim de jogo!')


        # Load objects of the game here
        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)

pygame.quit()
sys.exit()
