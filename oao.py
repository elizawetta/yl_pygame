import pygame
import os
import sys
import random


def load_image(name, folder='', colorkey=None):
    fullname = os.path.join(folder, name)
    if not os.path.isfile(fullname):
        sys.exit()

    image = pygame.image.load(fullname)
    return image


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Cube(pygame.sprite.Sprite):
    IMG = {'b': load_image('black.png', 'images'),
           'g': load_image('green.png', 'images'),
           'r': load_image('red.png', 'images'),
           'y': load_image('yellow.png', 'images'),
           's': load_image('sky.png', 'images')}

    def __init__(self, *group, **kwargs):
        '''pos: координаты, img: тип картинки'''
        super(Cube, self).__init__(*group)
        self.image = Cube.IMG[kwargs['img']]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = kwargs['pos'][0]
        self.rect.y = kwargs['pos'][1]

    def update(self, x):
        self.rect.x -= x


class Line(pygame.sprite.Sprite):
    def __init__(self, *group, **kwargs):
        super(Line, self).__init__(*group)
        self.image = pygame.Surface((50, 2))
        x, y = kwargs['pos'][0], kwargs['pos'][1]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()

    def update(self, x):
        self.rect.x -= x


class Chel(pygame.sprite.Sprite):
    IMG = {'sad': load_image('чел грустит.png', 'челикс'),
           'fun': load_image('чел с улыбкой.png', 'челикс'),
           'side': load_image('чел сбоку с улыбкой.png', 'челикс'), }

    def __init__(self, *group, **kwargs):
        super(Chel, self).__init__(*group)
        self.image = Chel.IMG['side']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 800 - 150 - 60
        self.height = self.image.get_height()
        self.width = self.image.get_width()


    def update(self, y):
        self.rect.y -= y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class ChelLine(pygame.sprite.Sprite):
    def __init__(self, *group, **kwargs):
        super(ChelLine, self).__init__(*group)
        self.image = pygame.Surface((20, 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 250 + 16
        self.rect.y = 800 - 150 - 60 + 62


    def update(self, y):
        self.rect.y -= y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

