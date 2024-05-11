import pygame
import game
import copy

class Pokemon(pygame.sprite.Sprite):

    def __init__(self, img, name, probability, max_hp, skills):
        pygame.sprite.Sprite.__init__(self)
        self.lvl = 1
        self.texture = img
        self.image = copy.copy(img)
        self.image.blit(game.pok_font.render(f"lvl:{self.lvl}", 1, "WHITE", "BLACK"), (0, 0))
        self.name = name
        self.probability = probability
        self.hp = 100
        self.max_hp = max_hp
        self.dmg_mlt = 1
        self.skills = skills
        self.dmg_hp = 0
        self.heal_hp = 0

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))
    
    def level_render(self):
        self.image = copy.copy(self.texture)
        self.image.blit(game.pok_font.render(f"lvl:{self.lvl}", 1, "WHITE", "BLACK"), (0, 0))

    def heal(self, hp):
        self.hp += hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        self.heal_hp = hp


    def deal_damage(self, hp):
        self.hp -= hp
        if self.hp < 0:
            self.hp = 0
        self.dmg_hp = hp

    def use_skill(self, number, enemy):
        self.heal(int(self.skills[number][0] * 1.1**self.lvl))
        enemy.deal_damage(int(self.skills[number][1] * 1.1**self.lvl))