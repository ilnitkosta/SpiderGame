import pygame
import sys
import random
#english version
#initialize pygame
pygame.init()

screen = pygame.display.set_mode((576, 1024))
title = pygame.display.set_caption('クモ対ヘビ - Spider vs Snakes')
clock = pygame.time.Clock()
game_font = pygame.font.Font('Fonts/SF-Pro.ttf', 40)

#game variables
gravity = 0.1  #reduced gravity
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

#functions
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_snake():
    random_snake_pos = random.choice(snake_height)
    bottom_snake = snake_surface.get_rect(midtop=(700, random_snake_pos))
    top_snake = snake_surface.get_rect(midbottom=(700, random_snake_pos - 300))
    return bottom_snake, top_snake

def move_snakes(snakes):
    for snake in snakes:
        snake.centerx -= 5
    visible_snakes = [snake for snake in snakes if snake.right > -50]
    return visible_snakes

def draw_snakes(snakes):
    for snake in snakes:
        if snake.bottom >= 1024:
            screen.blit(snake_surface, snake)
        else:
            flip_snake = pygame.transform.flip(snake_surface, False, True)
            screen.blit(flip_snake, snake)

def check_collision(snakes):
    for snake in snakes:
        if spider_rect.colliderect(snake):
            return False
    if spider_rect.top <= -100 or spider_rect.bottom >= 900:
        return False
    return True

#background and floor
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

#spider
spider_surface = pygame.transform.scale2x(pygame.image.load('assets/spider.png').convert_alpha())
spider_rect = spider_surface.get_rect(center=(100, 512))

#snakes
snake_surface = pygame.image.load('assets/snake_pipe.png')
snake_surface = pygame.transform.scale2x(snake_surface)
snake_list = []
SPAWNSNAKE = pygame.USEREVENT
pygame.time.set_timer(SPAWNSNAKE, 1200)
snake_height = [400, 600, 800]

#game over
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'スコア-Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def snake_score_check():
    global score, can_score
    if snake_list:
        for snake in snake_list:
            if 95 < snake.centerx < 105 and can_score:
                score += 1
                can_score = False
            if snake.centerx < 0:
                can_score = True

#main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                snake_list.clear()
                spider_rect.center = (100, 512)
                bird_movement = 0
                score = 0
        if event.type == SPAWNSNAKE:
            snake_list.extend(create_snake())

    screen.blit(bg_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        spider_rect.centery += bird_movement
        screen.blit(spider_surface, spider_rect)
        game_active = check_collision(snake_list)
        snake_list = move_snakes(snake_list)
        draw_snakes(snake_list)
        snake_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    draw_floor()
    pygame.display.update()
    clock.tick(120)
