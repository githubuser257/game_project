import pygame
import game
import copy
import random
import fight

class NPC(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = game.images["npc"]
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y


    def collide(self):
        if len(game.player.pokemons) == 0:
            return
        text_surface = pygame.surface.Surface((164, 31))
        text_surface.set_alpha(127)
        text_surface.blit(game.msg_font.render(("Press F to fight"), 1, "BLACK", "GREY"), (0, 0))
        game.screen.blit(text_surface, (220, 300))
        if game.is_pressed(pygame.K_f):
            current_enemy = copy.copy(random.choice(game.pokemons))
            current_enemy.lvl = random.randint(1, 5)
            current_enemy.level_render()
            game.current_fight = fight.Fight(copy.copy(game.player.pokemons[game.player.selected_pokemon_index]), current_enemy)
            game.current_npc = self
            game.game_state = "fight"
