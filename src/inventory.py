import pygame
import game

class Inventory:

    def __init__(self):
        self.backpack_image = pygame.surface.Surface((400, 300), pygame.SRCALPHA)
        self.is_open = False

    def update(self): 
        if game.is_pressed(pygame.K_e):
            self.is_open = not self.is_open
        if self.is_open:
            self.draw()

    def draw(self):
        self.backpack_image.fill((0, 0, 0, 0))
        self.backpack_image.blit(game.images["inventory_bg"], (0, 0))
        self.backpack_image.blit(game.text_font.render("Inventory", 1, "BLACK"), (130, 0))
        self.backpack_image.blit(game.text_font.render("Coins:", 1, "YELLOW"), (20, 250))
        self.backpack_image.blit(game.text_font.render(str(game.player.coins), 1, "YELLOW"), (110, 250))
        self.backpack_image.blit(game.text_font.render("Pokeballs:", 1, "BLUE"), (180, 250))
        self.backpack_image.blit(game.text_font.render(str(game.player.pokeballs), 1, "BLUE"), (330, 250))

        x_pok = 40
        y_pok = 50
        for pok in game.player.pokemons:
            pok.draw(self.backpack_image, x_pok, y_pok)
            x_pok += 80
            if x_pok == 360:
                y_pok += 80
                x_pok = 40
        game.screen.blit(self.backpack_image, (100, 50))
