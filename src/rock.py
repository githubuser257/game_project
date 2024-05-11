import pygame
import game

class Rock(pygame.sprite.Sprite):

    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = img
        self.rect = pygame.Rect(x, y, 32, 32)

    def collide(self):
        pass