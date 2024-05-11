import game
import json

def save_game():
    save = {}
    save["level"] = game.level_index
    save["coins"] = game.player.coins
    save["pokeballs"] = game.player.pokeballs
    save["x"] = game.player.rect.x
    save["y"] = game.player.rect.y
    save["npcs"] = game.beaten_npcs
    pokemon_list = []
    for pokemon in game.player.pokemons:
        pokemon_list.append([pokemon.name, pokemon.lvl])
    save["pokemons"] = pokemon_list
    with open("save.json", "w") as save_file:
        save_file.write(json.dumps(save))