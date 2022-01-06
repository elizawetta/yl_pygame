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
                Cube(cubes, pos=(col * 50 + 300, i * 50), img=el)
                end = max(end, col)


def draw_play_screen():
    screen.fill((204, 255, 255))
    pygame.draw.rect(screen, 'black', (0, 800 - 150, 1400, 150))
    cubes.draw(screen)
    chel.draw(screen)


def check_event(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        return True
    # if event.type == pygame.KEYDOWN:
    #     if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_w]:
    #         return True
    # return False


def check_jump():
    global in_jump, up_flag, up
    if in_jump and up_flag:
        chel.update(200 * seconds)
        up -= 200 * seconds
        if up <= 0:
            up_flag = False
            for i in chel:
                i.rect.y = 800 - 150 - 60 - 100
    if in_jump and not up_flag:
        chel.update(-200 * seconds)
        up += 200 * seconds
        if up >= 100:
            in_jump = False
            for i in chel:
                i.rect.y = 800 - 150 - 60


cubes = pygame.sprite.Group()
add_cubes('lvl_1.txt')
chel = pygame.sprite.Group()
Chel(chel)
draw_play_screen()

pygame.display.flip()
elapsed = 0
# clock = pygame.time.Clock()
end = end * 50 + 100
running = True
run_chel = False
in_jump = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if check_event(event):
            run_chel = True
            clock = pygame.time.Clock()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and run_chel and not in_jump:
            up, up_flag = 100, True
            in_jump = True
    if run_chel:
        seconds = elapsed / 1000.0
        end -= 200 * seconds
        elapsed = clock.tick(30)
        draw_play_screen()

        if end >= 0:
            cubes.update(200 * seconds)
        check_jump()
    
    pygame.display.flip()
