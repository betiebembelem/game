import pygame.time

import all_sprites_group
import player
from enemy import *
from player import *
from random import randint
from HUD import *

pygame.init()
pygame.display.set_caption('Игра Года')
clock = pygame.time.Clock()

all_sprites_group.add(player)

text_color = (255, 0, 0)
image_end = pygame.image.load('sprites/backgrounds/gameover.jpg')
image_start = pygame.image.load('sprites/backgrounds/back.png')


def enemy_outside_camera(randomx, randomy):
    return not(camera.offset.x <= randomx <= camera.offset.x + WIDTH and
               camera.offset.y <= randomy <= camera.offset.y + HEIGHT)


def random_pos():
    return randint(0, WIDTH * 2), randint(0, HEIGHT * 2)


def enemy_spawn(spawn_speed, wave, call_count):
    if wave == 1:
        spawn_speed += 0.5
    elif wave == 2:
        spawn_speed += 2
    elif wave == 3:
        spawn_speed += 20
    if spawn_speed > 200:
        randomx, randomy = random_pos()
        if enemy_outside_camera(randomx, randomy):
            Enemy((randomx, randomy))
        spawn_speed = 0
    if call_count % 200 == 0:
        randomx, randomy = random_pos()
        if enemy_outside_camera(randomx, randomy):
            Mage((randomx, randomy))
    return spawn_speed


def game():
    call_count = 1
    spawn_speed = 40

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        if player.player_data['get_hurt_count'] == player.player_data['health_amount']:
            return "game_end"

        if call_count == 1000:
            player.player_data['wave'] += 1
            call_count = 0

        if player.player_data['wave'] == 4:
            return 'game_end'

        screen.fill((0, 0, 0))
        camera.custom_draw(player)
        spawn_speed = enemy_spawn(spawn_speed, player.player_data['wave'], call_count)
        call_count += 1
        all_sprites_group.update()

        pygame.display.update()
        clock.tick(FPS)


def game_start():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1, 0, 0) and 440 <= mouse_x <= 840 and 280 <= mouse_y <= 360:
            return "game"

        screen.blit(image_start, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def game_end():
    text_surface = font.render(str(player.player_data['score']), True, text_color)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        screen.blit(image_end, (0, 0))
        screen.blit(text_surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


current_screen = "game_start"
while True:
    if current_screen == "game_start":
        current_screen = game_start()
    elif current_screen == "game":
        current_screen = game()
    elif current_screen == "game_end":
        current_screen = game_end()
