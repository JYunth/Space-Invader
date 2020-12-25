import pygame
import random
import math
from pygame import mixer

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
teal = (0, 128, 128)

# PyGame Initialization
pygame.init()

# Screen
screen_width = 800
screen_length = 600
screen = pygame.display.set_mode((screen_width, screen_length))

# Background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
window_icon = pygame.image.load('ufo.png')
pygame.display.set_icon(window_icon)

# Player
player_img = pygame.image.load('battleship.png')
player_x = 370
player_y = 480
playerx_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('ufo.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemyx_change.append(4)
    enemyy_change.append(40)

# Bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bulletx_change = 0
bullety_change = 10
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game over text

over_font = pygame.font.Font('freesansbold.ttf', 64)


# Definitions

def game_over_text():
    pygame.mixer.music.stop()
    over_text = over_font.render("GAME OVER", True, red)
    screen.blit(over_text, (210, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, white, )
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow((enemy_x - bullet_x), 2) + math.pow((enemy_y - bullet_y), 2))
    if distance <= 27:
        return True
    else:
        return False


# Main Gameloop
game_running = True
while game_running == True:

    screen.fill(black)
    # Adding the bg
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        # Keystroke checking
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5

            if event.key == pygame.K_RIGHT:
                playerx_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_x = player_x
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # Checking for boundaries of spaceship
    player_x += playerx_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemyx_change[i]

        if enemy_x[i] <= 0:
            enemyx_change[i] = 4
            enemy_y[i] += enemyy_change[i]
        elif enemy_x[i] >= 736:
            enemyx_change[i] = -4
            enemy_y[i] += enemyy_change[i]

        # Collision checking
        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
