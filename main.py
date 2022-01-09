import pygame
import os
import sys
import random

from oao import *

pygame.init()
pygame.display.set_caption('')
size = width, height = 1400, 800
screen = pygame.display.set_mode(size)
screen_speed = 200
chel_speed = 250


def add_cubes(file_name):
    file = open(file_name, 'r').readlines()
    file = list(map(lambda x: x.strip(), file))
    global end
    end = 0
    for i, row in enumerate(file):
        for col, el in enumerate(row):
            if el in 'bgyrs':
                Cube(cubes, pos=(col * 50 + 300, i * 50 + 150), img=el)
                Line(lines, pos=(col * 50 + 300, i * 50 + 150))

                end = max(end, col)


def check_event(event):
    # TODO: проверка на то, что мышка не находится на кнопках
    if event.type == pygame.MOUSEBUTTONDOWN:
        return True
    # if event.type == pygame.KEYDOWN:
    #     if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_w]:
    #         return True
    # return False


def check_jump(a):
    global in_jump, up_flag, up
    if in_jump and up_flag:
        chel.update(chel_speed * seconds)
        line_chel.update(chel_speed * seconds)
        up -= chel_speed * seconds
        if up <= 0:
            up_flag = False
            chel.rect.y = level- a
            line_chel.rect.y = level - a
    if in_jump and not up_flag:
        chel.update(-chel_speed * seconds)
        line_chel.update(-chel_speed * seconds)
        up += chel_speed * seconds
        if up >= a:
            in_jump = False
            up_flag = False
            chel.rect.y =  level
            line_chel.rect.y = level + chel.height


def check_cross():
    global in_jump
    global chel
    global level
    global run_chel
    for i in lines:
        if pygame.sprite.collide_mask(chel, i):
            if abs(chel.height + chel.rect.y - i.rect.y) < 4:
                level = chel.rect.y
                in_jump, up_flag = False, False
            else:
                run_chel = False
                # TODO: при столкновении на уровень опускаться


def draw_play_screen():
    screen.fill((204, 255, 255))
    pygame.draw.rect(screen, 'black', (0, height - 150, width, 150))
    sett_img = load_image('settings_img.png', 'images')
    pause_img = load_image('pause_img.png', 'images')
    repeat_img = load_image('repeat_img.png', 'images')

    screen.blit(sett_img, (10, 10))
    screen.blit(pause_img, (10, 60))
    screen.blit(repeat_img, (10, 110))

    lines.draw(screen)
    cubes.draw(screen)
    chel.draw(screen)
    line_chel.draw(screen)


cubes = pygame.sprite.Group()
lines = pygame.sprite.Group()
add_cubes('lvl_1.txt')
chel = Chel()
line_chel = ChelLine()

draw_play_screen()

pygame.display.flip()
elapsed = 0
end = end * 50 + 100
running = True
run_chel = False
in_jump = False
level = chel.rect.y
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if check_event(event):
            run_chel = not run_chel
            clock = pygame.time.Clock()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and run_chel and not in_jump:
            up, up_flag = 62, True
            in_jump = True
    if run_chel:
        seconds = elapsed / 1000.0
        end -= screen_speed * seconds
        elapsed = clock.tick(30)

        if end >= 0:
            cubes.update(screen_speed * seconds)
            lines.update(screen_speed * seconds)

        if in_jump:
            check_jump(62)
        check_cross()
    draw_play_screen()
    pygame.display.flip()
    # print(chel.rect)


