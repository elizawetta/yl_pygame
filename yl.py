import pygame
import os
import sys
import random

pygame.init()
pygame.display.set_caption('Boom them all')
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bomb(pygame.sprite.Sprite):
    bomb_image = load_image('bomb.png')
    boom_image = load_image('boom.png')

    def __init__(self, *group):
        super(Bomb, self).__init__(*group)
        self.image = Bomb.bomb_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - 50)
        self.rect.y = random.randrange(height - 50)

    def reset_img(self):
        self.image = Bomb.boom_image
        self.rect.x -= 30
        self.rect.y -= 30

    def check_pos(self, pos):
        if self.rect.collidepoint(pos) and self.image == Bomb.bomb_image:
            self.reset_img()


all_sprites = pygame.sprite.Group()
for i in range(20):
    Bomb(all_sprites)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in all_sprites:
                bomb.check_pos(pygame.mouse.get_pos())
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
