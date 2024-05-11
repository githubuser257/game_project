import pygame
import game

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = game.images["grass"]
        self.rect = self.image.get_rect()
    
    def collide(self):
        pass
