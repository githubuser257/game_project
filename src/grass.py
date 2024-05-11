import pygame
import game
import random

class Grass(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = game.images["tall_grass"]
        self.rect = pygame.Rect(x, y, 32, 32)
    
    def collide(self):
        if random.randint(1, 1000) == 1:
            if game.player.pokeballs > 0:
                game.current_pokemon = random.choice(game.pokemons)
                game.game_state = "get_pokemon"