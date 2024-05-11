import pygame
import game

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, font, text):
        pygame.sprite.Sprite.__init__(self)
        self.btn = pygame.surface.Surface((width, height))
        self.btn.fill(color)
        self.btn.blit(font.render(text, 1, "BLACK"), (10, 0))
        self.x = x
        self.y = y
        self.x1 = x + width
        self.y1 = y + height

    def draw(self):
        game.screen.blit(self.btn, (self.x, self.y))
    
    def is_clicked(self):
        for event in game.current_events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.x <= event.pos[0] <= self.x1 and self.y <= event.pos[1] <= self.y1:
                return True
        return False