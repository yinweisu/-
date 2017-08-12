# -*- coding: utf-8 -*-
import pygame
import random
from pygame.locals import *
from sys import exit
from Roles import *


BACKGROUND_IMG = 'resources/image/background.png'
SHOOT_IMG = 'resources/image/shoot.png'
GAME_OVER_IMG = 'resources/image/gameover.png'
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 480

# init
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('打飞机咯')
background = pygame.image.load(BACKGROUND_IMG)
shoot_img = pygame.image.load(SHOOT_IMG)
game_over = pygame.image.load(GAME_OVER_IMG)

# config player
player_imgs = []
player_rect = pygame.Rect(0, 99, 102, 126)      # from shoot.pack
player_imgs.append(shoot_img.subsurface(player_rect))
player_rect = pygame.Rect(165, 360, 102, 126)
player_imgs.append(shoot_img.subsurface(player_rect))
player_pos = [240, 600]
player = Player(player_pos, player_imgs)

# config bullet
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_image = shoot_img.subsurface(bullet_rect)
shoot_frequency = 0

# config enemy
enemy_rect = pygame.Rect(534, 612, 57, 43)
enemy_image = shoot_img.subsurface(enemy_rect)

enemy_down_images = []
enemy_down_rect = pygame.Rect(267, 347, 57, 43)
enemy_down_images.append(shoot_img.subsurface(enemy_rect))
enemy_down_rect = pygame.Rect(873, 697, 57, 43)
enemy_down_images.append(shoot_img.subsurface(enemy_rect))
enemy_down_rect = pygame.Rect(267, 296, 57, 43)
enemy_down_images.append(shoot_img.subsurface(enemy_rect))
enemy_down_rect = pygame.Rect(930, 697, 57, 43)
enemy_down_images.append(shoot_img.subsurface(enemy_rect))

enemy_x = random.randrange(0, SCREEN_WIDTH, 1)
enemy_y = 0
enemy_frequency = 0
enemies = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()

# config some shit
score = 0
running = True
frame_counter = 0

clock = pygame.time.Clock()
# main loop
while running:
    # 锁帧
    clock.tick(60)
    # 设置 frame counter
    frame_counter += 1
    if frame_counter == 10:
        frame_counter = 0
    # receive events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # create enemies
    if enemy_frequency % 25 == 0:
        enemy = Enemy((random.randrange(0 + enemy_rect.width, SCREEN_WIDTH - enemy_rect.width), 0), enemy_image, enemy_down_images)
        enemies.add(enemy)
    enemy_frequency += 1

    if enemy_frequency == 100:
        enemy_frequency = 0

    # keyboard interaction
    key_pressed = pygame.key.get_pressed()
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.move_right()

    # player shoot
    if not player.is_hit:
        if shoot_frequency % 15 == 0:
            player.shoot(bullet_image)
        shoot_frequency += 1
        if shoot_frequency == 15:
            shoot_frequency = 0

    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # blits the background
    window.fill(0)
    window.blit(background, (0, 0))

    # enemies moves and check collision
    for enemy in enemies:
        if pygame.sprite.collide_circle_ratio(0.7)(enemy, player):
            player.is_hit = True
            enemies_down.add(enemy)
            enemies.remove(enemy)
            break
        enemy.move()
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # 渲染击毁敌机
    for enemy in pygame.sprite.groupcollide(enemies, player.bullets, 1, 1):
        enemies_down.add(enemy)

    for enemy_down in enemies_down:
        if enemy_down.image_down_index == 0:
            pass
        if enemy_down.image_down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue

        window.blit(enemy_down.down_images[enemy_down.image_down_index // 2], enemy_down.rect)
        enemy_down.image_down_index += 1

    if player.is_hit:
        running = False

    # blits player
    window.blit(player.image[frame_counter // 5], player.rect)
    player.bullets.draw(window)
    enemies.draw(window)

    # 绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    window.blit(score_text, text_rect)

    pygame.display.update()

# Game Over!!!
font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = window.get_rect().centerx
text_rect.centery = window.get_rect().centery + 24
window.blit(game_over, (0, 0))
window.blit(text, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()