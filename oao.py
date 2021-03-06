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
        self.image.fill(self.get_color(kwargs['color']))
        x, y = kwargs['pos'][0], kwargs['pos'][1]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()

    def get_color(self, color):
        if color == 'r':
            return (255, 0, 0)
        if color == 'y':
            return (255, 255, 0)
        if color == 'g':
            return (0, 255, 0)
        return (0, 0, 0)

    def update(self, x):
        self.rect.x -= x


class Chel(pygame.sprite.Sprite):
    IMG = {'sad': load_image('чел грустит.png', 'челикс'),
           'fun': load_image('чел с улыбкой.png', 'челикс'),
           'side': load_image('чел сбоку с улыбкой.png', 'челикс')}

    def __init__(self, *group, **kwargs):
        super(Chel, self).__init__(*group)
        self.image = Chel.IMG['side']
        self.mask = pygame.mask.from_surface(self.image)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 800 - 150 - self.height + 2

    def update(self, y):
        self.rect.y -= y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
