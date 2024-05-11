import pygame
import game
import init

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = game.images["exit"]
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y
    
    def collide(self):
        if (not game.cheats) and (game.npc_count > 0):
            return
        text_surface = pygame.surface.Surface((315, 31))
        text_surface.set_alpha(127)
        text_surface.blit(game.msg_font.render(("Press F to go to the next level"), 1, "BLACK", "GREY"), (0, 0))
        game.screen.blit(text_surface, (150, 300))
        if game.is_pressed(pygame.K_f):
            game.level_index += 1
            if game.level_index >= len(game.levels):
                game.game_state = "end"
                return
            init.init_game()
            init.init_pokemons()
            game.player.rect.x = 64
            game.player.rect.y = 64
