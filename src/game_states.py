import pygame
import game
import random
import copy
from button import Button
import init
import save

def check_pokemon(name):
    for i, pok in enumerate(game.player.pokemons):
        if pok.name == name:
            return i
    return -1


def menu():
    game.screen.blit(game.images["brick_bg"], (0, 0))
    game.screen.blit(game.title_font.render("Game", 1, "BLACK"), (20, 0))
    if len(game.buttons) == 0:
        game.buttons.append(Button(20, 100, 250, 80, "GREY", game.menu_font, "New game"))
        game.buttons.append(Button(20, 200, 250, 80, "GREY", game.menu_font, "Load game"))
    for btn in game.buttons:
        btn.draw()
    if game.buttons[0].is_clicked():
        game.buttons.clear()
        init.init_game()
        init.init_pokemons()
        game.game_state = "gameplay"
    elif game.buttons[1].is_clicked():
        game.buttons.clear()
        init.init_save()
        game.game_state = "gameplay"
    

def pause():
    if len(game.buttons) == 0:
        game.buttons.append(Button(220, 100, 150, 50, "GREY", game.pause_font, "Continue"))
        game.buttons.append(Button(185, 200, 220, 50, "GREY", game.pause_font, "Save and quit"))
    for btn in game.buttons:
        btn.draw()
    if game.buttons[0].is_clicked():
        game.buttons.clear()
        game.game_state = "gameplay"
    elif game.buttons[1].is_clicked():
        game.buttons.clear()
        save.save_game()
        game.game_state = "quit"
    if game.is_pressed(pygame.K_ESCAPE):
        game.game_state = "gameplay"

def mining():
    game.screen.blit(game.images["brick_bg"], (0, 0))
    game.screen.blit(game.text_font.render(("Mine"), 1, "BLACK"), (10, 10))
    game.screen.blit(game.text_font.render((f"Coins: {game.player.coins}"), 1, "BLACK"), (430, 10))
    if game.is_pressed(pygame.K_SPACE):
        game.player.coins += 1
    
    game.screen.blit(game.text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))
    if game.is_pressed(pygame.K_q):
        game.game_state = "gameplay"


def gameplay():
    if game.is_pressed(pygame.K_ESCAPE):
        background = pygame.surface.Surface((game.screen_width, game.screen_height), pygame.SRCALPHA)
        background.fill("GREY")
        background.set_alpha(127)
        game.screen.blit(background, (0, 0))
        game.game_state = "pause"
        return
    
    game.screen.fill((0, 180, 0))
    for e in game.all_sprites:
        game.screen.blit(e.image, game.camera.apply(e))

    inventory_icon = pygame.Surface((80, 80))
    inventory_icon.fill("BROWN")
    e_text = game.text_font.render("E", 1, "BLACK")
    inventory_icon.blit(e_text, (30, 20))
    game.screen.blit(inventory_icon, (0, 320))

    if len(game.player.pokemons) != 0:
        selected_name = game.player.pokemons[game.player.selected_pokemon_index].name
        game.screen.blit(game.select_pok_font.render(f"<- R | Selected Pokemon: {selected_name}| T -> ", 1, "BLACK"), (120, 370))
    if game.is_pressed(pygame.K_t):
        game.player.selected_pokemon_index += 1
        if game.player.selected_pokemon_index >= len(game.player.pokemons):
            game.player.selected_pokemon_index = 0
    if game.is_pressed(pygame.K_r):
        game.player.selected_pokemon_index -= 1
        if game.player.selected_pokemon_index < 0:
            game.player.selected_pokemon_index = len(game.player.pokemons) - 1

    game.player.update()
    game.camera.update()
    game.inventory.update()


def get_pokemon():
    game.screen.blit(game.images["brick_bg"], (0, 0))
    game.current_pokemon.draw(game.screen, 400, 100)
    game.screen.blit(game.text_font.render((f"{game.current_pokemon.probability}%"), 1, "BLACK"), (400, 170))
    game.screen.blit(game.text_font.render((f"F - use pokeball"), 1, "BLACK"), (50, 300))
    game.screen.blit(game.text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if game.is_pressed(pygame.K_f):
        game.player.pokeballs -= 1
        random_number = random.randint(1, 100)
        if random_number <= game.current_pokemon.probability:
            pokemon_index = check_pokemon(game.current_pokemon.name)
            if pokemon_index == -1:
                game.player.pokemons.append(copy.copy(game.current_pokemon))
            else:
                game.player.pokemons[pokemon_index].lvl += 1
                game.player.pokemons[pokemon_index].level_render()
            game.game_state = "success_pokemon"
        else:
            game.game_state = "fail_pokemon"
    
    if game.is_pressed(pygame.K_q):
        game.game_state = "gameplay"
    

def success_pokemon():
    game.screen.blit(game.images["brick_bg"], (0, 0))
    game.screen.blit(game.text_font.render((f"You got a pokemon!"), 1, "BLACK"), (150, 180))
    game.screen.blit(game.text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if game.is_pressed(pygame.K_q):
        game.game_state = "gameplay"


def fail_pokemon():
    game.screen.blit(game.images["brick_bg"], (0, 0))
    game.screen.blit(game.text_font.render((f"The pokemon ran away!"), 1, "BLACK"), (150, 180))
    game.screen.blit(game.text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if game.is_pressed(pygame.K_q):
        game.game_state = "gameplay"


def fight():
    game.current_fight.render()
    game.current_fight.fight()


def win():
    game.screen.blit(game.images["brick_bg"], (0, 0))
    game.screen.blit(game.text_font.render((f"You win!"), 1, "BLACK"), (150, 180))
    game.screen.blit(game.text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if game.is_pressed(pygame.K_q):
        game.game_state = "gameplay"


def lose():
    game.screen.blit(game.images["brick_bg"], (0, 0))
    game.screen.blit(game.text_font.render((f"You lose!"), 1, "BLACK"), (150, 180))
    game.screen.blit(game.text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if game.is_pressed(pygame.K_q):
        game.game_state = "gameplay"

def end():
    game.screen.blit(game.images["brick_bg"], (0, 0))
    game.screen.blit(game.text_font.render((f"The end"), 1, "BLACK"), (210, 150))
    game.screen.blit(game.text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if game.is_pressed(pygame.K_q):
        game.game_state = "quit"