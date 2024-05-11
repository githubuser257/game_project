import pygame
import game

class Block(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 16
        self.height = 16
        self.image = game.images["brick"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def collide(self):
        game.player.rect.x -= game.player.xvel
        game.player.rect.y -= game.player.yvel
