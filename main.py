import pygame
import os
import sys
import random

from oao import *

pygame.init()
pygame.display.set_caption('')
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
screen_speed = 200
chel_speed = 250


def begin_play():
    global cubes, lines, chel
    global run_chel, in_jump, start_play
    global score, end, level
    cubes = pygame.sprite.Group()
    lines = pygame.sprite.Group()
    add_cubes('lvl_1.txt')
    chel = Chel()

    elapsed = 0
    score = 0
    run_chel = False
    in_jump = False
    start_play = True
    level = chel.rect.y


def get_points(color):
    if color == (255, 0, 0):
        return -5
    if color == (255, 255, 0):
        return 5
    if color == (0, 255, 0):
        return 10
    return 0


def add_cubes(file_name):
    file = open(file_name, 'r').readlines()
    file = list(map(lambda x: x.strip(), file))
    global end
    end = 0
    for i, row in enumerate(file):
        for col, el in enumerate(row):
            if el in 'bgyrs':
                Cube(cubes, pos=(col * 50 + 250, i * 50 + 150), img=el)
                Line(lines, pos=(col * 50 + 250, i * 50 + 150), color=el)

                end = max(end, col)
    end = end * 50 - 50


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
    global in_jump, up_flag, up
    global chel
    global level, score
    global run_chel, start_play
    for i in lines:
        if pygame.sprite.collide_mask(chel, i):
            if abs(chel.rect.y + chel.height - i.rect.y) < 4:
                chel.rect.y = i.rect.y - chel.height + 2
                level = chel.rect.y
                in_jump, up_flag = False, False
                color = i.image.get_at((1, 1))[:3]
                score += get_points(color)
            else:
                run_chel = False
                # TODO: при столкновении на уровень опускаться
            return
    if not in_jump:
        in_jump, up_flag, up = True, False, 65
        level += 50
        lines.update(5)
        cubes.update(5)
        check_jump(65)


def draw_score(screen):
    font = pygame.font.Font(None, 50)
    text1 = font.render(f'Score: {score}', False, '#44FF00')
    text2 = font.render(f'Score: {score}', False, (0, 0, 0))
    text_x = 10
    text_y = 10

    screen.blit(text2, (text_x + 2, text_y + 2))
    screen.blit(text1, (text_x, text_y))


def start_game(open_img, back_img):
    for i in range(255, -1, -5):
        screen.fill((255, 255, 255))
        if i < 120:
            draw_play_screen(screen)
        img = open_img.copy()
        img2 = back_img.copy()
        img.set_alpha(i)
        img2.set_alpha(i)
        screen.blit(img2, (0, 0))
        screen.blit(img, ((width - 425) // 2, (height - 155) // 2))
        pygame.display.flip()
        pygame.time.delay(1)


def draw_play_screen(screen):
    global start_play
    screen.fill((204, 255, 255))
    pygame.draw.rect(screen, 'black', (0, height - 150, width, 150))

    # screen.blit(sett_img, (10, 10))
    screen.blit(pause if run_chel else play, (width - 40 - 10 - 50, 10))
    screen.blit(repeat, (width - 40 - 10 , 10))

    lines.draw(screen)
    cubes.draw(screen)
    chel.draw(screen)
    draw_score(screen)

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

open_img = load_image('open.png', 'images')
back_img = load_image('img.png', 'images')

run_chel = False
in_jump = False
start_play = True
level = chel.rect.y
zero_lvl = level
score = 0
open_flag = False
screen.blit(back_img, (0, 0))
screen.blit(open_img, ((width - 425) // 2, (height - 155) // 2))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if open_flag:
                start_game(open_img, back_img)
                open_flag = False
                continue
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
    if open_flag:
        continue
    if run_chel:
        seconds = elapsed / 1000.0
        end -= screen_speed * seconds
        elapsed = clock.tick(30)

        if in_jump:
            check_jump(65)
        check_cross()
        if end > 0:
            cubes.update(screen_speed * seconds)
            lines.update(screen_speed * seconds)
        if end <= 0:
            run_chel = False
            chel.rect.y = zero_lvl

    draw_play_screen(screen)
    pygame.display.flip()
