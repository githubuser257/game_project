import pygame
import game

class Shop(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 64
        self.height = 64
        self.image = game.images["shop"]
        self.rect = (pygame.Rect(x, y, self.width, self.height))
        self.msg = ""

    def collide(self):
        if self.rect.colliderect(game.player):
            game.print_msg("Press F to exchange 15 coins for 1 pokeball", 95, 300)
            animation_tick = game.get_tick("msg")
            if self.msg != "":
                game.print_msg(self.msg, 190, 350, 127 - animation_tick * 2)
            if animation_tick >= 63:
                self.msg = ""
            if game.is_pressed(pygame.K_f):
                if game.player.coins >= 15:
                    game.player.coins -= 15
                    game.player.pokeballs += 1
                    self.msg = "You bought a pokeball!"
                else:
                    self.msg = "You don't have money!"
                game.set_tick("msg")