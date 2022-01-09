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


def begin_play():
    global cubes, lines, chel, end, run_chel, in_jump, level, start_play
    cubes = pygame.sprite.Group()
    lines = pygame.sprite.Group()
    add_cubes('lvl_1.txt')
    chel = Chel()

    elapsed = 0
    end = end * 50 + 100
    run_chel = False
    in_jump = False
    start_play = True
    level = chel.rect.y


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


def check_jump(a):
    global in_jump, up_flag, up
    if in_jump and up_flag:
        chel.update(chel_speed * seconds)
        up -= chel_speed * seconds
        if up <= 0:
            up_flag = False
            chel.rect.y = level - a
    if in_jump and not up_flag:
        chel.update(-chel_speed * seconds)
        up += chel_speed * seconds
        if up >= a:
            in_jump = False
            up_flag = False
            chel.rect.y = level


def check_cross():
    global in_jump
    global chel
    global level
    global run_chel, start_play
    for i in lines:
        if pygame.sprite.collide_mask(chel, i):
            if abs(chel.height + chel.rect.y - i.rect.y) < 4:
                level = chel.rect.y
                in_jump, up_flag = False, False
            else:
                run_chel = False
                # TODO: при столкновении на уровень опускаться


def draw_play_screen():
    global start_play
    screen.fill((204, 255, 255))
    pygame.draw.rect(screen, 'black', (0, height - 150, width, 150))

    screen.blit(sett_img, (10, 10))
    screen.blit(pause if run_chel else play, (10, 60))
    screen.blit(repeat, (10, 110))

    lines.draw(screen)
    cubes.draw(screen)
    chel.draw(screen)

    if not run_chel:
        s = pygame.Surface((width, height))
        s.set_alpha(125)
        s.fill((255, 255, 255))
        screen.blit(s, (0, 0))
        if not start_play:
            screen.blit(play_img, (450, 100))
            screen.blit(repeat_img, (700, 100))
        elif start_play:
            screen.blit(play_img, (700 - 125, 100))


sett_img = load_image('settings_img.png', 'images')
pause_img = load_image('pause.png', 'images')
play_img = load_image('play.png', 'images')
repeat_img = load_image('repeat.png', 'images')

play = pygame.transform.scale(play_img, (40, 40))
pause = pygame.transform.scale(pause_img, (40, 40))
repeat = pygame.transform.scale(repeat_img, (40, 40))

cubes = pygame.sprite.Group()
lines = pygame.sprite.Group()
add_cubes('lvl_1.txt')
chel = Chel()

elapsed = 0
end = end * 50 + 100

run_chel = False
in_jump = False
start_play = True
level = chel.rect.y
draw_play_screen()
pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 10 <= x <= 50 and 60 <= y <= 100:
                run_chel = not run_chel
                if run_chel:
                    clock = pygame.time.Clock()
            if 110 <= y <= 150 and 10 <= x <= 50:
                begin_play()
            if start_play and 700 - 125 <= x <= 700 - 125 + 225 and 100 <= y <= 325:
                start_play = False
                run_chel = True
                clock = pygame.time.Clock()
            elif not start_play and 450 <= x <= 450 + 225 and 100 <= y <= 325:
                start_play = False
                run_chel = True
                clock = pygame.time.Clock()
            elif not start_play and 700 <= x <= 700 + 225 and 100 <= y <= 325:
                begin_play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and run_chel and not in_jump:
            up, up_flag = 65, True
            in_jump = True
    if run_chel:
        seconds = elapsed / 1000.0
        end -= screen_speed * seconds
        elapsed = clock.tick(30)

        if end >= 0:
            cubes.update(screen_speed * seconds)
            lines.update(screen_speed * seconds)

        if in_jump:
            check_jump(65)
        check_cross()
    draw_play_screen()
    pygame.display.flip()
