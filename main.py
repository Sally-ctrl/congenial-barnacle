from operator import truediv

import pygame
import random
import math
from pygame import  mixer
mixer.init()
game_over_played = False


# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# initializ pygame

pygame.init()
clock = pygame.time.Clock()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
Background = pygame.image.load("background.jpg")
Background = pygame.transform.scale(Background, (800, 600))

# title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player
PlayerImg = pygame.image.load("ship.png")
PlayerImg = pygame.transform.scale(PlayerImg, (64, 64))

PlayerX = 370
PlayerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 10
for i in range(num_of_enemies):
    # enemy
    enemyImg1 = pygame.image.load("ufo.png")
    enemyImg.append(pygame.transform.scale(enemyImg1, (64, 64)))

    enemyX.append(random.randint(0+i*5, 736))
    enemyY.append(random.randint(50+i*10, 150+i*20))
    enemyX_change.append(random.choice([-3, -2,1, 2, 3,5,7]))
    enemyY_change.append(20)

# bullet
# enemy
# ready= cant see the bullet
# fire= bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletImg = pygame.transform.scale(bulletImg, (32, 32))

#bulletX = 0
#bulletY = 480
bullets = []
bulletY_change = 15

# Enemy bullets
bulletenemyIMG = pygame.image.load("bullet2.png")
bulletenemyIMG= pygame.transform.scale(bulletenemyIMG, (32, 32))
enemy_bullets=[]
bullet_change = 15




# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score2 = font.render("Score:" + str(score), True, (255, 255, 255))
    screen.blit(score2,(textX,textY))

def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullets.append([x+16,y+10]) # add bullet position to the list


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    return False

overFont=pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text= overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text,(200,300))
def fireenemy(enemyX,enemyY):
    enemy_bullets.append([enemyX+16,enemyY+64])

 

def is_enemy_collision(bulletX,bulletY,PlayerX,PlayerY):
    if bulletX ==PlayerX and bulletY == PlayerY:
        return True
    return False

#  Timing for random enemy shooting
enemy_bullet_delay = 1000  # milliseconds between enemy shots
last_enemy_shot_time = pygame.time.get_ticks() # returns how many milliseconds have passed since the game started.



# Game loop


running = True
while running:
    screen.fill((192, 192, 192))
    # background image
    screen.blit(Background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE :
                mixer.Sound('laser.wav').play()
                fire_bullet(PlayerX, PlayerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    PlayerX += playerX_change
    if PlayerX <= 0:
        PlayerX = 0
    if PlayerX >= 736:
        PlayerX = 736

    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_shot_time > enemy_bullet_delay:
        shooter = random.randint(0, num_of_enemies - 1)
        fireenemy(enemyX[shooter], enemyY[shooter])
        last_enemy_shot_time = current_time


    # enemy bullets
    for bullet in enemy_bullets[:]:
        if bullet[1] >= 600:
            enemy_bullets.remove(bullet)
        if isCollision(PlayerX + 16, PlayerY + 32, bullet[0], bullet[1]):
            game_over_text()
            pygame.display.update()
            if not game_over_played:
                mixer.Sound('you-lose-female-gfx-sounds-1-1-00-01.mp3').play()
                game_over_played = True
                pygame.time.delay(2000)
                running= False

            #enemy_bullets.remove(bullet)




    # enemymovement
    for i in range(num_of_enemies):



        # game over
        if enemyY[i]>=410:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            if not game_over_played:
                mixer.Sound('you-lose-female-gfx-sounds-1-1-00-01.mp3').play()
                game_over_played = True

            break




        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        #  check for collision
        for bullet in bullets[:]:
            collision = isCollision(enemyX[i], enemyY[i], bullet[0], bullet[1])
            if collision:
                mixer.Sound('explosion.wav').play()
                bullets.remove(bullet)
                score += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    for bullet in bullets[:]:
        bullet[1]-=bulletY_change
        if bullet[1]<=0:
            bullets.remove(bullet)
    # Draw bullets
    for bullet in bullets:
        screen.blit(bulletImg, (bullet[0], bullet[1]))
    for bullet in enemy_bullets:
        bullet[1] += 5
    for bullet in enemy_bullets:
        screen.blit(bulletenemyIMG, (bullet[0], bullet[1]))

    player(PlayerX, PlayerY)
    show_score(textX,textY)
    pygame.display.update()
    clock.tick(60)  # limits loop to 60 frames per second
