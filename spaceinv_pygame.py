from sys import exit
import random
import pygame
import time


pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)
background_img = pygame.image.load('stars.jpg').convert()
background_img = pygame.transform.scale(background_img, (800, 600))
background_x = 0
background_y = 0

clock = pygame.time.Clock()

# player
player_img = pygame.image.load('space-invaders.png')
player_x = 370
player_y = 480
player_x_change = 0

# bullet
bullet_img = pygame.image.load('bullet.png')
bullet_state = 'ready'
bullet_x = player_x
bullet_y = player_y
bullet_y_change = 0

# enemy
enemy1_img = pygame.image.load('alien.png')
enemy1_x = []
[enemy1_x.append(random.randint(336, 736)) for i in range(3)]
enemy1_y = []
[enemy1_y.append(random.randint(0, 150)) for i in range(3)]

x_change1 = 1
y_change1 = 0

enemy2_img = pygame.image.load('alien2rs.png')
enemy2_x = []
[enemy2_x.append(random.randint(0, 400)) for i in range(3)]
enemy2_y = []
[enemy2_y.append(random.randint(0, 150)) for i in range(3)]

x_change2 = -1
y_change2 = 0


def player():
    screen.blit(player_img, (player_x, player_y))


def bullet():
    screen.blit(bullet_img, (bullet_x, bullet_y))


def enemy():

    for i in range(len(enemy1_x)):
        screen.blit(enemy1_img, (enemy1_x[i], enemy1_y[i] + y_change1))

    for i in range(len(enemy2_x)):
        screen.blit(enemy2_img, (enemy2_x[i], enemy2_y[i] + y_change2))

        if enemy1_y[i] + y_change1 >= 400 or enemy2_y[i] + y_change2 >= 400:
            print('game over')
            return False


def background():
    screen.blit(background_img, (background_x, background_y))
    screen.blit(background_img, (background_x, background_y - 600))


def collision():

    for i in range(len(enemy1_x)):

        d1 = ((enemy1_x[i] - bullet_x)**2 +
              (enemy1_y[i] - bullet_y)**2)**(1/2)

        if d1 <= 50:
            print(str(i) + ' d1 hit: ' + str(d1))
            enemy1_x[i] = random.randint(336, 736)
            enemy1_y[i] = random.randint(0, 150)
            return True

    for i in range(len(enemy2_x)):
        d2 = ((enemy2_x[i] - bullet_x)**2 +
              (enemy2_y[i] - bullet_y)**2)**(1/2)

        if d2 <= 50:
            print(str(i) + ' d2 hit: ' + str(d2))
            enemy2_x[i] = random.randint(0, 400)
            enemy2_y[i] = random.randint(0, 150)
            return True


active = True
score = 0
# game loop
while active:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_x_change = 2
            if event.key == pygame.K_LEFT:
                player_x_change = -2
            if event.key == pygame.K_SPACE:
                bullet_state = 'fire'
                bullet_y_change = -15

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_x_change = 0

            if event.key == pygame.K_LEFT:
                player_x_change = 0

    # background movement
    background_y += 2
    background()

    if background_y >= 600:
        background_y = 0

    # player
    player_x += player_x_change
    player()

    if player_x <= 0 or player_x >= 736:
        player_x_change = 0

    # enemy movement
    for i in range(len(enemy1_x)):

        enemy1_x[i] += x_change1

        if enemy1_x[i] >= 736:
            x_change1 = -1
            y_change1 += 20

        elif enemy1_x[i] <= 0:
            x_change1 = 1
            y_change1 += 20

    for i in range(len(enemy2_x)):

        enemy2_x[i] += x_change2

        if enemy2_x[i] <= 0:
            x_change2 = 1
            y_change2 += 20

        elif enemy2_x[i] >= 700:
            x_change2 = -1
            y_change2 += 20

    enemy()

    # bullets
    if bullet_state == 'fire':
        bullet_y += bullet_y_change
        bullet_x = player_x - player_x_change
        bullet()
        if bullet_y <= 0:
            bullet_state = 'ready'
            bullet_y = player_y
        if collision():
            bullet_state = 'ready'
            bullet_y = player_y
            score += 1
            time.sleep(0.5)
            print('SCORE: ' + str(score))

    if enemy() == False:
        active = False

    pygame.display.update()
    clock.tick(120)
