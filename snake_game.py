import pygame
import random
import os

pygame.init()

# Screen
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 12

font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 40)

# 🔊 Sound (optional)
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
except:
    eat_sound = None

# 🏆 High Score File
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

def get_highscore():
    with open("highscore.txt", "r") as f:
        return int(f.read())

def save_highscore(score):
    if score > get_highscore():
        with open("highscore.txt", "w") as f:
            f.write(str(score))

def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, green, (block[0], block[1], snake_block, snake_block))

def show_score(score):
    text = font.render("Score: " + str(score), True, white)
    high = font.render("High: " + str(get_highscore()), True, white)
    screen.blit(text, (10, 10))
    screen.blit(high, (450, 10))

# 🟢 START SCREEN
def start_screen():
    while True:
        screen.fill(black)

        title = big_font.render("SNAKE GAME", True, green)
        screen.blit(title, (150, 120))

        msg = font.render("Press SPACE to Start", True, white)
        screen.blit(msg, (170, 200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

# 🎮 MAIN GAME
def game():
    x = width // 2
    y = height // 2
    dx = 0
    dy = 0

    snake = []
    length = 1

    foodx = random.randrange(0, width - snake_block, snake_block)
    foody = random.randrange(0, height - snake_block, snake_block)

    game_over = False

    while True:

        # 💀 GAME OVER SCREEN
        while game_over:
            screen.fill(black)

            msg = big_font.render("GAME OVER", True, red)
            screen.blit(msg, (180, 150))

            restart = font.render("Press R to Restart", True, white)
            screen.blit(restart, (180, 200))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -snake_block; dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = snake_block; dy = 0
                elif event.key == pygame.K_UP:
                    dy = -snake_block; dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = snake_block; dx = 0

        x += dx
        y += dy

        # Wall collision
        if x < 0 or x >= width or y < 0 or y >= height:
            save_highscore(length - 1)
            game_over = True

        screen.fill(black)

        # 🍎 Food
        pygame.draw.circle(screen, red, (foodx + 5, foody + 5), 5)

        head = [x, y]
        snake.append(head)

        if len(snake) > length:
            del snake[0]

        # Self collision
        for block in snake[:-1]:
            if block == head:
                save_highscore(length - 1)
                game_over = True

        draw_snake(snake)

        # Eat food
        if x == foodx and y == foody:
            foodx = random.randrange(0, width - snake_block, snake_block)
            foody = random.randrange(0, height - snake_block, snake_block)
            length += 1
            if eat_sound:
                eat_sound.play()

        show_score(length - 1)

        pygame.display.update()
        clock.tick(snake_speed)

# ▶️ RUN
start_screen()
game()