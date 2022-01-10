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
    global run_chel, in_jump, start_play, end_game
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
    end_game = 0
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
    global in_jump, up_flag, up, end_game
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
                end_game = -1
            return
    if not in_jump:
        in_jump, up_flag, up = True, False, 65
        level += 50
        lines.update(5)
        cubes.update(5)
        check_jump(65)


def draw_score(screen):
    font = pygame.font.Font('font.ttf', 50)
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


def draw_res(x1, y1, img1, x2, y2, img2, delay):
    pygame.time.delay(delay)
    for i in range(0, 255, 10):
        img_1 = img1.copy()
        img_2 = img2.copy()
        img_1.set_alpha(i)
        img_2.set_alpha(i)
        screen.blit(img1, (x1, y1))
        screen.blit(img2, (x2, y2))
        pygame.display.flip()
        pygame.time.delay(10)


def draw_play_screen(screen):
    global start_play
    screen.fill((204, 255, 255))
    pygame.draw.rect(screen, 'black', (0, height - 150, width, 150))

    # screen.blit(sett_img, (10, 10))
    screen.blit(pause if run_chel else play, (width - 100, 10))
    screen.blit(repeat, (width - 50, 10))

    lines.draw(screen)
    cubes.draw(screen)
    chel.draw(screen)
    draw_score(screen)

    if not run_chel:
        s = pygame.Surface((width, height))
        s.set_alpha(125)
        s.fill((255, 255, 255))
        screen.blit(s, (0, 0))
        if end_game == -1 or end_game == 1:
            font = pygame.font.Font('font.ttf', 50)
            if end_game == 1:
                delay = 400
                img = load_image('game_over_nice.png', 'images')
                text1 = font.render(f'Ура, победа!!!', False, (0, 0, 0))
                text2 = font.render(f'Score: {score}', False, (0, 0, 0))
            else:
                delay = 100
                img = load_image('game_over_bad.png', 'images')
                text1 = font.render(f'Вы проиграли!', False, (0, 0, 0))
                text2 = font.render(f'Score: {score}', False, (0, 0, 0))
            img.blit(text1, ((img.get_width() - text1.get_width()) // 2, 100))
            img.blit(text2, ((img.get_width() - text2.get_width()) // 2, 200))
            x_1, y_1 = ((width - img.get_width()) // 2, 80)
            x_2, y_2 = ((width - 225) // 2, 430)
            draw_res(x_1, y_1, img, x_2, y_2, repeat_img, delay)


        elif not start_play:
            screen.blit(play_img, (width // 2 - 225, 200))
            screen.blit(repeat_img, (width // 2, 200))

        elif start_play:
            screen.blit(play_img, ((width - 225) // 2, 200))


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
open_flag = True
end_game = 0
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
            if 10 <= y <= 50 and width - 100 <= x <= width - 60:
                run_chel = not run_chel
                if run_chel:
                    clock = pygame.time.Clock()
            elif width - 50 <= x <= width - 10 and 10 <= y <= 50:
                begin_play()
            elif start_play and not run_chel and \
                    (width - 225) // 2 <= x <= (width - 225) // 2 + 225 and 200 <= y <= 425:
                start_play = False
                run_chel = True
                clock = pygame.time.Clock()
            elif not start_play and end_game == 0 \
                    and width // 2 - 225 <= x <= width // 2 and 200 <= y <= 425:
                start_play = False
                run_chel = True
                clock = pygame.time.Clock()
            elif not start_play and end_game == 0 \
                    and width // 2 <= x <= width // 2 + 225 and 200 <= y <= 425:
                begin_play()
            elif (end_game == -1 or end_game == 1) \
                    and (width - 225) // 2 <= x <= (width - 225) // 2 + 225 and 430 <= y <= 430 + 225:
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
            end_game = 1

    draw_play_screen(screen)
    pygame.display.flip()
