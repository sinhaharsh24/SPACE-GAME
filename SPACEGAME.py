import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Game")
icon = pygame.image.load('img/spaceship.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('img/spacegamebg.png')
bg = pygame.transform.scale(background, (800, 600))
q = 0
height = 600

# Player
playerimg = pygame.image.load('img/spaceshipplayer.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

# enemy
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('img/spaceshipenemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
bullet = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # ready - we can't see the bullet on the screen

# score
score = 0
font = pygame.font.Font('font/Coffee Spark.ttf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('font/Coffee Spark.ttf', 64)


def show_score(x, y):
    scorefinal = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(scorefinal, (x, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 18, y + 20))


run = True
while run:

    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, q))
    screen.blit(background, (0, height + q))

    if q == -height:
        screen.blit(background, (0, height + q))
        q = 0
    q -= 1

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # creating boundry for game
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 720:
        playerX = 720

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            show_score(textX, textY)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 720:
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        # collison
        collison = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Draw the player
    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()

pygame.quit()
