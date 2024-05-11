import pygame
import game

class Mine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 80
        self.height = 80
        self.image = game.images["mine"]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def collide(self):
        game.print_msg("Press F to enter the mine", 170, 300)
        if game.is_pressed(pygame.K_f):
            game.game_state = "mining"
