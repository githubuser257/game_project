import pygame
import game

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.coins = 0
        self.pokeballs = 0
        self.image = game.images["player_right_1"]
        self.speed = 6
        self.rect = self.image.get_rect()
        self.rect.x += 64
        self.rect.y += 64
        self.pokemons = []
        self.selected_pokemon_index = 0
        self.last_img = "player_right_"
        if game.cheats:
            self.coins = 100
            self.pokeballs = 100

    def update(self):
        keyboard = pygame.key.get_pressed()
        self.xvel = 0
        self.yvel = 0
        
        if keyboard[pygame.K_a]:
            self.xvel += -self.speed
        if keyboard[pygame.K_d]:
            self.xvel += self.speed

        self.rect.x += self.xvel
        self.collide()

        if keyboard[pygame.K_w]:
            self.yvel += -self.speed
        if keyboard[pygame.K_s]:
            self.yvel += self.speed

        animation_tick = game.get_tick("player")

        if animation_tick == 6:
            game.set_tick("player")
            game.move_index += 1
            game.move_index = game.move_index % 3

        if self.xvel > 0:
            self.last_img = "player_right_"
            game.player.image = game.images[f"player_right_{game.move_index + 1}"]
        elif self.xvel < 0:
            self.last_img = "player_left_"
            game.player.image = game.images[f"player_left_{game.move_index + 1}"]
        elif self.yvel != 0:
            game.player.image = game.images[f"{self.last_img}{game.move_index + 1}"]
        else:
            game.player.image = game.images[f"{self.last_img}1"]
            game.stop_tick("player")
            game.move_index = 0

        self.xvel = 0

        self.rect.y += self.yvel
        self.collide()
        self.yvel = 0
    

    def collide(self):
        for sprite in game.sprites:
            if self.rect.colliderect(sprite):
                sprite.collide()
