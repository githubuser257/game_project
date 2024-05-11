import pygame
import json
import copy

pygame.init()

PL_HEIGHT, PL_WIDTH = 32, 32
screen_width = 600
screen_height = 400
text_font = pygame.font.SysFont("comicsans", 32)
msg_font = pygame.font.SysFont("comicsans", 22)
pok_font = pygame.font.SysFont("comicsans", 16)
select_pok_font = pygame.font.SysFont("comicsans", 20)
dmg_font = pygame.font.SysFont("comicsans", 16)
menu_font = pygame.font.SysFont("comicsans", 48)
pause_font = pygame.font.SysFont("comicsans", 32)
title_font = pygame.font.SysFont("comicsans", 64)

game_state = "menu"
player = None
inventory = None
all_sprites = pygame.sprite.Group()
sprites = []
pokemons = []
current_events = []
current_pokemon = None
current_fight = None
current_npc = None
level_index = 0
npc_count = 0
move_index = 0
game_tick = 0
animation_ticks = {}
buttons = []
beaten_npcs = []
all_pokemons = []
cheats = False

with open("./levels.json") as levels_file:
    levels = json.load(levels_file)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
total_level_width = 32
total_level_height = 32
camera = None

def get_pokemon_by_name(name):
    for pokemon in all_pokemons:
        if pokemon.name == name:
            return copy.copy(pokemon)

def set_tick(name):
    animation_ticks[name] = game_tick

def get_tick(name):
    if not (name in animation_ticks):
        return 0
    if animation_ticks[name] == -1:
        set_tick(name)
    return game_tick - animation_ticks[name]

def stop_tick(name):
    animation_ticks[name] = -1


def print_text(msg, x, y, font, color, alpha=255):
        current_surface = pygame.surface.Surface((1000, 500), pygame.SRCALPHA)
        current_surface.fill((0, 0, 0, 0))
        current_surface.blit(font.render(str(msg), 1, color), (0, 0))
        current_surface.set_alpha(alpha)
        screen.blit(current_surface, (x, y))

def print_msg(msg, x, y, alpha=127):
    text_surface = pygame.surface.Surface((1000, 500), pygame.SRCALPHA)
    text_surface.fill((0, 0, 0, 0))
    text_surface.set_alpha(alpha)
    text_surface.blit(msg_font.render((msg), 1, "BLACK", "GREY"), (0, 0))
    screen.blit(text_surface, (x, y))


def is_pressed(key):
    for event in current_events:
        if event.type == pygame.KEYDOWN and event.key == key:
            current_events.remove(event)
            return True
    return False


def transform_image(img, width, height):
    return pygame.transform.scale(img, (width, height))

images = {
    "grass": transform_image(pygame.image.load("./images/grass.png"), 2400, 1600),
    "brick": transform_image(pygame.image.load("./images/brick.png"), 32, 32),
    "tall_grass": pygame.image.load("./images/tall_grass.png"),
    "shop": transform_image(pygame.image.load("./images/shop_2.png"), 64, 64),
    "mine": transform_image(pygame.image.load("./images/mine.png"), 96, 96),
    "rock_1": transform_image(pygame.image.load("./images/rock_1.png"), 24, 16),
    "rock_2": transform_image(pygame.image.load("./images/rock_2.png"), 12, 8),
    "player_left_1": transform_image(pygame.image.load("./images/player_left_1.png"), 25, 45),
    "player_left_2": transform_image(pygame.image.load("./images/player_left_2.png"), 25, 45),
    "player_left_3": transform_image(pygame.image.load("./images/player_left_3.png"), 25, 45),
    "player_right_1": transform_image(pygame.image.load("./images/player_right_1.png"), 25, 45),
    "player_right_2": transform_image(pygame.image.load("./images/player_right_2.png"), 25, 45),
    "player_right_3": transform_image(pygame.image.load("./images/player_right_3.png"), 25, 45),
    "brick_bg": transform_image(pygame.image.load("images/brick_bg.png"), 600, 400),
    "npc": transform_image(pygame.image.load("images/npc.png"), 32, 32),
    "exit": transform_image(pygame.image.load("images/exit.png"), 64, 64),
    "inventory_bg": transform_image(pygame.image.load("images/inventory_bg.png"), 400, 300)
}