import pygame
import game
import game_states
from player import Player
from inventory import Inventory
from camera import Camera
import init
import sys

def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "cheats":
        game.cheats = True
    game.player = Player()
    game.inventory = Inventory()
    game.camera = Camera(Camera.camera_configure, game.total_level_width, game.total_level_height)
    init.init_all_pokemons()
    run = True
    while run:
        game.current_events = pygame.event.get()
        if game.game_state == "menu":
            game_states.menu()
        elif game.game_state == "pause":
            game_states.pause()
        elif game.game_state == "gameplay":
            game_states.gameplay()
        elif game.game_state == "mining":
            game_states.mining()
        elif game.game_state == "get_pokemon":
            game_states.get_pokemon()
        elif game.game_state == "success_pokemon":
            game_states.success_pokemon()
        elif game.game_state == "fail_pokemon":
            game_states.fail_pokemon()
        elif game.game_state == "fight":
            game_states.fight()
        elif game.game_state == "win":
            game_states.win()
        elif game.game_state == "lose":
            game_states.lose()
        elif game.game_state == "end":
            game_states.end()
        else:
            run = False
        
        game.game_tick += 1

        for event in game.current_events:
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        game.clock.tick(60)

if __name__ == "__main__":
    main()