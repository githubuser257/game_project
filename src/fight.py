import pygame
import game
import random

class Fight:

    def __init__(self, pok, enemy):
        self.pok = pok
        self.enemy = enemy
        self.last_msg = ""
        pass

    def render(self):
        game.screen.blit(game.images["brick_bg"], (0, 0))
        game.print_text(self.last_msg, 0, 0, game.text_font, "BLACK")
        game.screen.blit(self.pok.image, (50, 200))
        game.print_text(self.pok.hp, 50, 150, game.text_font, "BLACK")
        game.print_text(self.pok.name, 50, 265, game.text_font, "BLACK")
        game.screen.blit(self.enemy.image, (500, 200))
        game.print_text(self.enemy.hp, 495, 150, game.text_font, "BLACK")
        game.print_text(self.enemy.name, 440, 265, game.text_font, "BLACK")
        animation_tick = game.get_tick("fight")
        if self.pok.dmg_hp != 0:
            game.print_text(f"-{self.pok.dmg_hp}", 50, 140 - animation_tick, game.dmg_font, "RED", 256 - animation_tick * 9)
        if self.pok.heal_hp != 0:
            game.print_text(f"+{self.pok.heal_hp}", 80, 140 - animation_tick, game.dmg_font, "BLUE", 256 - animation_tick * 9)
        if self.enemy.dmg_hp != 0:
            game.print_text(f"-{self.enemy.dmg_hp}", 495, 140 - animation_tick, game.dmg_font, "RED", 256 - animation_tick * 9)
        if self.enemy.heal_hp != 0:
            game.print_text(f"+{self.enemy.heal_hp}", 525, 140 - animation_tick, game.dmg_font, "BLUE", 256 - animation_tick * 9)
        if animation_tick == 30:
            self.pok.dmg_hp = 0
            self.pok.heal_hp = 0
            self.enemy.dmg_hp = 0
            self.enemy.heal_hp = 0
    
    
    def fight(self):
        if game.is_pressed(pygame.K_1):
            self.pok.use_skill(0, self.enemy)
            self.check()
            if game.game_state != "fight":
                return
            self.use_enemy_skill()
            self.check()
            game.set_tick("fight")
        if game.is_pressed(pygame.K_2):
            self.pok.use_skill(1, self.enemy)
            self.check()
            if game.game_state != "fight":
                return
            self.use_enemy_skill()
            self.check()
            game.set_tick("fight")
    

    def use_enemy_skill(self):
        skill_number = random.randint(0, 1)
        self.enemy.use_skill(skill_number, self.pok)
        if skill_number == 0:
            self.last_msg = f"Enemy attacked!"
        if skill_number == 1:
            self.last_msg = f"Enemy healed!"
    

    def check(self):
        if self.pok.hp == 0:
            game.game_state = "lose"
        if self.enemy.hp == 0:
            game.beaten_npcs.append([game.current_npc.rect.x, game.current_npc.rect.y])
            game.all_sprites.remove(game.current_npc)
            game.sprites.remove(game.current_npc)
            game.game_state = "win"
            game.npc_count -= 1
