import pygame
import math
import time
from utilities import *
import random

color = {"red": (255, 0, 0), "blue": (0, 0, 255),
         "light_blue": (173, 216, 230), "yellow": (255, 249, 10),
         "dark_brown": (77, 38, 2), "brown": (247, 125, 10),
         "orange": (247, 46, 10), "yellow": (247, 239, 10),
         "bright_blue": (10, 247, 208), "lilac": (247, 10, 232),
         "pink": (247, 10, 10), "grey": (150, 150, 150),
         "light_grey": (210, 210, 210), "bright_green": (0, 255, 0),
         "green": (0, 150, 0), "bright_red": (255, 0, 0), "red": (200, 0, 0)}
letters = 'abcdefghijklmnopqrstuvwxyz'
pygame.init()
largeText = pygame.font.Font('freesansbold.ttf', 100)
mediumText = pygame.font.Font('freesansbold.ttf', 45)
smallText = pygame.font.Font('freesansbold.ttf', 20)
correct = 0
total = 0
wrong = 0
distance = (85, 150)
time_pause = 1
white = (255, 255, 255)
black = (0, 0, 0)
display_width = 800
display_height = 800
display_center = (display_width//2, display_height//2)
clock = pygame.time.Clock()
def_font = pygame.font.get_default_font()
gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay.fill(white)
# Messages
messages = {'title_msg': Message(gameDisplay, "Widen your angle vision",
                                 'freesansbold.ttf', 30, (display_width/2,
                                                          display_height//8),
                                 color['blue'], white),
            'instruction_msg': Message(gameDisplay, "Focus your eyes on the
                                       green circle and type the popping-up
                                       symbols", 'freesansbold.ttf', 20,
                                       (display_width/2, display_height//4),
                                       color['blue'], white),
            'pick_level_msg': Message(gameDisplay, "Pick your training level",
                                      'freesansbold.ttf', 25,
                                      (display_width//2,
                                       display_height//2 - 70),
                                      color['blue'], white)}


def set_message(msg):
    return messages[msg]


def get_score(surface, font_size, coords):
    global total, correct, wrong
    missed = total - correct - wrong
    x, y = coords
    text1 = f'total = {total}'
    text2 = f'correct = {correct}, wrong = {wrong}, missed = {missed}'
    font = pygame.font.Font(def_font, font_size)
    total_text = font.render(text1, False, black)
    surface.blit(total_text, coords)
    correct_text = font.render(text2, False, black)
    surface.blit(correct_text, (x, y + font_size+10))
    pygame.display.update()


def set_level(level):
    distance = None
    if level == 1:
        distance = (85, 150)
        time_pause = 1
    elif level == 2:
        distance = (95, 200)
        time_pause = 2
    else:
        distance = (100, 280)
        time_pause = 2
    return distance, time_pause


def quit_game():
    pygame.quit()
    quit()


def game_intro():
    global distance, time_pause
    run_btn = Button(150, 700, 100, 50, color['blue'], color['light_blue'],
                     "Run", game_loop)
    quit_btn = Button(550, 700, 100, 50, color['red'], color['bright_red'],
                      "Quit", quit_game)
    pick_level_scale = Scale(gameDisplay, 100, display_height/2 - 25, 600, 40,
                             1, 1, 3, 1, color['red'], black, color['yellow'],
                             color['blue'])
    pick_level_scale.set_scale()
    title_msg = set_message('title_msg')
    instruction_msg = set_message('instruction_msg')
    pick_level_msg = set_message('pick_level_msg')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pick_level_scale.check_scale(event)
            run_btn.button_check(event)
            quit_btn.button_check(event)
        gameDisplay.fill(white)
        title_msg.display_msg()
        instruction_msg.display_msg()
        pick_level_msg.display_msg()
        pick_level_scale.display_scale()
        level = pick_level_scale.get_choice()
        distance, time_pause = set_level(level)
        run_btn.button_draw(gameDisplay)
        quit_btn.button_draw(gameDisplay)
        pygame.display.update()
        clock.tick(10)


def game_pause():
    global distance, time_pause
    global continue_btn, quit_btn
    continue_btn = Button(150, 700, 100, 50, color['blue'],
                          color['light_blue'], "Continue", game_loop)
    quit_btn = Button(550, 700, 100, 50, color['red'], color['bright_red'],
                      "Quit", quit_game)
    pick_level_scale = Scale(gameDisplay, 100, display_height/2 - 25, 600,
                             40, 1, 1, 3, 1, color['red'], black,
                             color['yellow'], color['blue'])
    pick_level_scale.set_scale()
    title_msg = set_message('title_msg')
    pick_level_msg = set_message('pick_level_msg')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pick_level_scale.check_scale(event)
            continue_btn.button_check(event)
            quit_btn.button_check(event)
        gameDisplay.fill(white)
        title_msg.display_msg()
        pick_level_msg.display_msg()
        pick_level_scale.display_scale()
        level = pick_level_scale.get_choice()
        distance, time_pause = set_level(level)
        continue_btn.button_draw(gameDisplay)
        quit_btn.button_draw(gameDisplay)
        pygame.display.update()
        clock.tick(10)


def get_background(width, height):
    symbol_surface = pygame.Surface((width, height))
    symbol_surface.fill(white)
    circ = pygame.draw.circle(symbol_surface, color['green'],
                              display_center, 45)
    return symbol_surface


def update_surface(surf):
    surf.fill(white)
    pygame.draw.circle(surf, color['green'], display_center, 45)


def get_coords():
    global distance
    x_center, y_center = display_center
    start, end = distance
    theta = random.randint(0, 360)
    r = random.randint(start, end)
    x = int(r * math.cos(theta)) + x_center
    y = int(r * math.sin(theta)) + y_center
    return x, y


def get_symbol():
    return letters[random.randint(0, 24)]


def game_loop():
    global total, correct, wrong
    global time_pause
    pause_btn = Button(325, 700, 100, 50, color['blue'], color['light_blue'],
                       "Pause", game_pause)
    symbol_surf = get_background(display_width, display_height - 110)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == text:
                    correct += 1
                if pygame.key.name(event.key) != text:
                    wrong += 1
            pause_btn.button_check(event)
        gameDisplay.fill(white)
        pause_btn.button_draw(gameDisplay)
        gameDisplay.blit(symbol_surf, (0, 0))
        x, y = get_coords()
        text = get_symbol()
        msg = Message(gameDisplay, text, 'freesansbold.ttf', 30,
                      (x, y), color['blue'], white)
        msg.display_msg()
        total += 1
        get_score(gameDisplay, 20, (10, 10))
        pygame.display.update()
        clock.tick(time_pause)

game_intro()






    


        
