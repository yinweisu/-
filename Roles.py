import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, images):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 15
        self.bullets = pygame.sprite.Group()
        self.image = []
        self.is_hit = False
        for i in images:
            self.image.append(i)
        self.rect = self.image[0].get_rect()
        self.rect.midbottom = (self.x, self.y)

    def update_pos(self):
        self.rect.midbottom = (self.x, self.y)

    def move_up(self):
        if not self.rect.top <= 0:
            self.y -= self.speed
        self.update_pos()

    def move_down(self):
        if not self.rect.bottom >= 800:
            self.y += self.speed
        self.update_pos()

    def move_left(self):
        if not self.rect.left <= 0:
            self.x -= self.speed
        self.update_pos()

    def move_right(self):
        if not self.rect.right >= 480:
            self.x += self.speed
        self.update_pos()

    def shoot(self, bullet_image):
        self.mid = self.rect.left + (self.rect.width / 2)
        bullet = Bullets(self.mid, self.rect.top, bullet_image)
        self.bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image, down_images):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 8
        self.is_hit = False
        self.image = image
        self.rect = image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        self.down_images = down_images
        self.image_down_index = 0

    def update_pos(self):
        self.rect.midbottom = (self.x, self.y)

    def move(self):
        self.y += self.speed
        self.update_pos()


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = 10
        self.image = image
        self.rect = image.get_rect()
        self.rect.midbottom = (x, y)

    def update_pos(self):
        self.rect.midbottom = (self.x, self.y)

    def move(self):
        self.y -= self.speed
        self.update_pos()