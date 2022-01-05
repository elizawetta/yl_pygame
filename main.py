import pygame
import os
import sys
import random

from oao import *

pygame.init()
pygame.display.set_caption('')
size = width, height = 1400, 800
screen = pygame.display.set_mode(size)


def add_cubes(file_name):
    file = open(file_name, 'r').readlines()
    file = list(map(lambda x: x.strip(), file))
    global end
    end = 0
    for i, row in enumerate(file):
        for col, el in enumerate(row):
            if el in 'bgyrs':
                Cube(cubes, pos=(col * 50 , i * 50), img=el)
                end = max(end, col)


def draw_play_screen():
    screen.fill((204, 255, 255))
    pygame.draw.rect(screen, 'black', (0, 800 - 150, 1400, 150))
    cubes.draw(screen)
    chel.draw(screen)
    pygame.display.flip()


cubes = pygame.sprite.Group()
add_cubes('lvl_1.txt')
chel = pygame.sprite.Group()
Chel(chel)
draw_play_screen()

pygame.display.flip()
x, elapsed = 0, 0
# clock = pygame.time.Clock()
end = end * 50 - 200
running = True
run_man = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            run_man = True
            clock = pygame.time.Clock()
    if run_man:
        seconds = elapsed / 1000.0
        x += 200 * seconds
        elapsed = clock.tick(30)
        draw_play_screen()

        if x < end:
            cubes.update(200 * seconds)
