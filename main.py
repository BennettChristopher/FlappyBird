import pygame
import sys
import random


# drawing/moving objects
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 540))
    screen.blit(floor_surface, (floor_x_pos + 480, 540))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 640:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx == -600:
            pipes.remove(pipe)
    return pipes


# collision detection
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):  # collision detection(overlapping)
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 540:
        return False

    return True


# animation
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


# score
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = font0.render(
            str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(240, 125))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = font0.render(
            f'score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(240, 475))
        screen.blit(score_surface, score_rect)

        high_score_surface = font0.render(
            f'high score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(240, 520))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# start/initialisation
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((480, 640))  # resolution
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(pygame.image.load(
    'resources/images/bird-downflap.png').convert_alpha())
clock = pygame.time.Clock()
font0 = pygame.font.Font('resources/fonts/04B_19.ttf', 35)
font1 = pygame.font.Font('resources/fonts/04B_19.ttf', 25)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# surfaces
# background
bg_surface = pygame.image.load('resources/images/background.png').convert()

# floor
floor_surface = pygame.image.load('resources/images/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# bird
bird_downflap = pygame.transform.scale2x(pygame.image.load(
    'resources/images/bird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(
    'resources/images/bird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(
    'resources/images/bird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(96, 320))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

bird_surface = pygame.image.load(
    'resources/images/bird-midflap.png').convert_alpha()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(96, 320))

# pipe
pipe_surface = pygame.image.load('resources/images/pipe.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 425, 450, 475, 500]

# information
info_surface = font1.render(f"Press ESC to quit the game...",
                            True, (255, 255, 255))
info_rect = info_surface.get_rect(center=(240, 60))
icon_surface = font1.render(f"Space",
                            True, (255, 255, 255))
icon_rect = icon_surface.get_rect(center=(240, 375))

# game over
game_over_surface = pygame.transform.scale2x(
    pygame.image.load('resources/images/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(240, 220))

# sounds
flap_sound = pygame.mixer.Sound('resources/sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('resources/sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('resources/sounds/sfx_point.wav')
score_sound_countdown = 100

# main gameloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (96, 320)
                bird_movement = 0
                score = 0
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))
    floor_surface.blit(info_surface, info_rect)

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(icon_surface, icon_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -480:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)
