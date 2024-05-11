import pygame
import game
import copy
from camera import Camera
from pokemon import Pokemon
from block import Block
from rock import Rock
from grass import Grass
from ground import Ground
from mine import Mine
from shop import Shop
from npc import NPC
from exit_sprite import Exit
import random
import json

def init_pokemons():
    pokemon_list = game.levels[game.level_index][1]
    game.pokemons = []
    for pokemon in pokemon_list:
        current_image = game.transform_image(pygame.image.load(pokemon[1]), 70, 70)
        current_pokemon = Pokemon(current_image, pokemon[0], pokemon[2], pokemon[3], pokemon[4])
        game.pokemons.append(current_pokemon)
    if game.cheats:
        game.player.pokemons.append(copy.copy(game.pokemons[0]))
        game.player.pokemons[-1].lvl = 10
        game.player.pokemons[-1].level_render()


def init_all_pokemons():
    for level in game.levels:
        current_pokemon_list = level[1]
        for pokemon in current_pokemon_list:
            current_image = game.transform_image(pygame.image.load(pokemon[1]), 70, 70)
            current_pokemon = Pokemon(current_image, pokemon[0], pokemon[2], pokemon[3], pokemon[4])
            game.all_pokemons.append(current_pokemon)


def init_game():
    game.level = game.levels[game.level_index][0]
    game.total_level_width = len(game.level[0]) * 32
    game.total_level_height = len(game.level) * 32
    game.camera = Camera(Camera.camera_configure, game.total_level_width, game.total_level_height)
    game.beaten_npcs.clear()

    for sprite in game.all_sprites:
        sprite.kill()
    game.sprites.clear()
    x = y = 0
    ground = Ground(0, 0)
    game.sprites.append(ground)
    for row in game.level:
        for col in row:

            if col == "n":
                if [x, y] in game.beaten_npcs:
                    col = " "
                else:
                    npc = NPC(x, y)
                    game.sprites.append(npc)
                    game.npc_count += 1

            if col == " ":
                random_number = random.randint(1, 100)
                if random_number <= 2:
                    rock = Rock(x, y, game.images[f"rock_{random_number}"])
                    game.sprites.insert(1, rock)
            
            if col == "-":
                block = Block(x, y)
                game.sprites.append(block)

            if col == "!":
                grass = Grass(x, y)
                game.sprites.append(grass)

            if col == "m":
                mine = Mine(x, y)
                game.sprites.append(mine)

            if col == "$":
                shop = Shop(x, y)
                game.sprites.append(shop)

            if col == "e":
                exit_sprite = Exit(x, y)
                game.sprites.append(exit_sprite)

            x += game.PL_WIDTH
        y += game.PL_HEIGHT
        x = 0
    for sprite in game.sprites:
        game.all_sprites.add(sprite)
    game.all_sprites.add(game.player)


def init_save():
    with open("./save.json", "r") as save_file:
        save = json.load(save_file)
    game.level_index = save["level"]
    game.player.coins = int(save["coins"])
    game.player.pokeballs = int(save["pokeballs"])
    game.player.rect.x = int(save["x"])
    game.player.rect.y = int(save["y"])
    game.beaten_npcs = save["npcs"]
    pokemon_list = save["pokemons"]
    for pokemon in pokemon_list:
        current_pokemon = game.get_pokemon_by_name(pokemon[0])
        current_pokemon.lvl = int(pokemon[1])
        current_pokemon.level_render()
        game.player.pokemons.append(current_pokemon)
    init_game()
    init_pokemons()