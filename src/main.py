import pygame
import random
import json
import copy

pygame.init()
pygame.display.set_caption("Pokemons")
PL_HEIGHT, PL_WIDTH = 32, 32
text_font = pygame.font.SysFont("comicsansms", 32)
msg_font = pygame.font.SysFont("comicsansms", 22)
pok_font = pygame.font.SysFont("comicsansms", 16)
select_pok_font = pygame.font.SysFont("comicsansms", 20)
dmg_font = pygame.font.SysFont("comicsansms", 16)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.coins = 0
        self.pokeballs = 0
        self.image = images["player_right_1"]
        self.speed = 6
        self.rect = self.image.get_rect()
        self.rect.x += 64
        self.rect.y += 64
        self.pokemons = []
        self.selected_pokemon_index = 0
        self.game_state = "gameplay"
        self.last_img = "player_right_"

    def update(self):
        global move_tick, move_index
        keyboard = pygame.key.get_pressed()
        self.xvel = 0
        self.yvel = 0
        
        if keyboard[pygame.K_a]:
            self.xvel += -self.speed
        if keyboard[pygame.K_d]:
            self.xvel += self.speed

        if move_tick == 6:
            move_tick = 0
            move_index += 1
            move_index = move_index % 3

        self.rect.x += self.xvel
        self.collide()

        if keyboard[pygame.K_w]:
            self.yvel += -self.speed
        if keyboard[pygame.K_s]:
            self.yvel += self.speed

        if self.xvel > 0:
            self.last_img = "player_right_"
            player.image = images[f"player_right_{move_index + 1}"]
            move_tick += 1
        elif self.xvel < 0:
            self.last_img = "player_left_"
            player.image = images[f"player_left_{move_index + 1}"]
            move_tick += 1
        elif self.yvel != 0:
            player.image = images[f"{self.last_img}{move_index + 1}"]
            move_tick += 1
        else:
            player.image = images[f"{self.last_img}1"]
            move_tick = 0
            move_index = 0

        self.xvel = 0

        self.rect.y += self.yvel
        self.collide()
        self.yvel = 0
    

    def collide(self):
        for sprite in sprites:
            if self.rect.colliderect(sprite):
                sprite.collide()


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images["grass"]
        self.rect = pygame.Rect(x, y, 600, 400)
    
    def collide(self):
        pass


class Pokemon(pygame.sprite.Sprite):

    def __init__(self, img, name, probability, max_hp, skills):
        pygame.sprite.Sprite.__init__(self)
        self.lvl = 1
        self.texture = img
        self.image = copy.copy(img)
        self.image.blit(pok_font.render(f"lvl:{self.lvl}", 1, "WHITE", "BLACK"), (0, 0))
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
        self.image.blit(pok_font.render(f"lvl:{self.lvl}", 1, "WHITE", "BLACK"), (0, 0))

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


class Block(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 16
        self.height = 16
        self.image = images["brick"]
        # self.rect = pygame.Rect(x, y, 16, 16)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def collide(self):
        player.rect.x -= player.xvel
        player.rect.y -= player.yvel


class Shop(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 64
        self.height = 64
        self.image = images["shop"]
        self.rect = (pygame.Rect(x, y, self.width, self.height))
        self.msg = ""

    def collide(self):
        global msg_tick
        if self.rect.colliderect(player):
            text_surface = pygame.surface.Surface((446, 31))
            text_surface.set_alpha(127)
            text_surface.blit(msg_font.render(("Press F to exchange 15 coins for 1 pokeball"), 1, "BLACK", "GREY"), (0, 0))
            screen.blit(text_surface, (95, 300))
            if self.msg != "":
                text_surface_2 = pygame.surface.Surface((11 * len(self.msg), 31))
                text_surface_2.fill("GREY")
                text_surface_2.set_alpha(127 - msg_tick * 2)
                text_surface_2.blit(msg_font.render((self.msg), 1, "BLACK", "GREY"), (0, 0))
                screen.blit(text_surface_2, (190, 350))
            if msg_tick >= 63:
                self.msg = ""
            if is_pressed(pygame.K_f):
                if player.coins >= 15:
                    player.coins -= 15
                    player.pokeballs += 1
                    self.msg = "You bought a pokeball!"
                else:
                    self.msg = "You don't have money!"
                msg_tick = 0
                

class Mine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 80
        self.height = 80
        self.image = images["mine"]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def collide(self):
        text_surface = pygame.surface.Surface((265, 31))
        text_surface.set_alpha(127)
        text_surface.blit(msg_font.render(("Press F to enter the mine"), 1, "BLACK", "GREY"), (0, 0))
        screen.blit(text_surface, (170, 300))
        if is_pressed(pygame.K_f):
            player.game_state = "mining"


class Grass(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = images["tall_grass"]
        self.rect = pygame.Rect(x, y, 32, 32)
    
    def collide(self):
        if random.randint(1, 1000) == 1:
            if player.pokeballs > 0:
                global current_pokemon
                current_pokemon = random.choice(pokemons)
                player.game_state = "get_pokemon"


class Rock(pygame.sprite.Sprite):

    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = img
        self.rect = pygame.Rect(x, y, 32, 32)

    def collide(self):
        pass


class NPC(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 32
        self.height = 32
        self.image = images["npc"]
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y


    def collide(self):
        if len(player.pokemons) == 0:
            return
        text_surface = pygame.surface.Surface((164, 31))
        text_surface.set_alpha(127)
        text_surface.blit(msg_font.render(("Press F to fight"), 1, "BLACK", "GREY"), (0, 0))
        screen.blit(text_surface, (220, 300))
        if is_pressed(pygame.K_f):
            current_enemy = copy.copy(random.choice(pokemons))
            current_enemy.lvl = random.randint(1, 5)
            current_enemy.level_render()
            global current_fight
            current_fight = Fight(copy.copy(player.pokemons[player.selected_pokemon_index]), current_enemy)
            global current_npc
            current_npc = self
            player.game_state = "fight"


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images["exit"]
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y
    
    def collide(self):
        if npc_count > 0:
            return
        text_surface = pygame.surface.Surface((315, 31))
        text_surface.set_alpha(127)
        text_surface.blit(msg_font.render(("Press F to go to the next level"), 1, "BLACK", "GREY"), (0, 0))
        screen.blit(text_surface, (150, 300))
        if is_pressed(pygame.K_f):
            global level_index
            level_index += 1
            if level_index >= len(levels):
                player.game_state = "end"
                return
            init_game()
            init_pokemons()
            player.rect.x = 64
            player.rect.y = 64
        

class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self):
        self.state = self.camera_func(self.state, player.rect)

    def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + 600 / 2, -t + 400/ 2

        l = min(0, l)
        l = max(-(camera.width - 600), l)
        t = max(-(camera.height - 400), t)
        t = min(0, t)

        return pygame.Rect(l, t, w, h)


class Inventory:

    def __init__(self):
        self.backpack_image = pygame.Surface((400, 300))
        self.backpack_image.fill("BROWN")
        self.is_open = False

    def update(self):
        if is_pressed(pygame.K_e):
            self.is_open = not self.is_open
        if self.is_open:
            self.draw()

    def draw(self):
        screen.blit(self.backpack_image, (100, 50))
        self.backpack_image.fill("BROWN")
        self.backpack_image.blit(text_font.render("Inventory", 1, "BLACK"), (130, 0))
        self.backpack_image.blit(text_font.render("Coins:", 1, "YELLOW"), (0, 250))
        self.backpack_image.blit(text_font.render(str(player.coins), 1, "YELLOW"), (90, 250))
        self.backpack_image.blit(text_font.render("Pokeballs:", 1, "BLUE"), (180, 250))
        self.backpack_image.blit(text_font.render(str(player.pokeballs), 1, "BLUE"), (330, 250))

        x_pok = 40
        y_pok = 50
        for pok in player.pokemons:
            pok.draw(self.backpack_image, x_pok, y_pok)
            x_pok += 80
            if x_pok == 360:
                y_pok += 80
                x_pok = 40


class Fight:

    def __init__(self, pok, enemy):
        self.pok = pok
        self.enemy = enemy
        self.last_msg = ""
        pass

    def render(self):
        screen.blit(images["brick_bg"], (0, 0))
        screen.blit(text_font.render(self.last_msg, 1, "BLACK"), (0, 0))
        screen.blit(self.pok.image, (50, 200))
        screen.blit(text_font.render(f"{self.pok.hp}", 1, "BLACK"), (50, 150))
        screen.blit(text_font.render(f"{self.pok.name}", 1, "BLACK"), (50, 265))
        screen.blit(self.enemy.image, (500, 200))
        screen.blit(text_font.render(f"{self.enemy.hp}", 1, "RED"), (495, 150))
        screen.blit(text_font.render(f"{self.enemy.name}", 1, "BLACK"), (440, 265))
        global dmg_tick
        if self.pok.dmg_hp != 0:
            screen.blit(dmg_font.render(f"-{self.pok.dmg_hp}", 1, "RED"), (50, 140 - dmg_tick))
        if self.pok.heal_hp != 0:
            screen.blit(dmg_font.render(f"+{self.pok.heal_hp}", 1, "BLUE"), (80, 140 - dmg_tick))
        if self.enemy.dmg_hp != 0:
            screen.blit(dmg_font.render(f"-{self.enemy.dmg_hp}", 1, "RED"), (495, 140 - dmg_tick))
        if self.enemy.heal_hp != 0:
            screen.blit(dmg_font.render(f"+{self.enemy.heal_hp}", 1, "BLUE"), (525, 140 - dmg_tick))
        if dmg_tick == 30:
            self.pok.dmg_hp = 0
            self.pok.heal_hp = 0
            self.enemy.dmg_hp = 0
            self.enemy.heal_hp = 0
        dmg_tick += 1
    
    
    def fight(self):
        global dmg_tick
        if is_pressed(pygame.K_1):
            self.pok.use_skill(0, self.enemy)
            self.check()
            if player.game_state != "fight":
                return
            self.use_enemy_skill()
            self.check()
            dmg_tick = 0
        if is_pressed(pygame.K_2):
            self.pok.use_skill(1, self.enemy)
            self.check()
            if player.game_state != "fight":
                return
            self.use_enemy_skill()
            self.check()
            dmg_tick = 0
    

    def use_enemy_skill(self):
        skill_number = random.randint(0, 1)
        self.enemy.use_skill(skill_number, self.pok)
        if skill_number == 0:
            self.last_msg = f"Enemy attacked!"
        if skill_number == 1:
            self.last_msg = f"Enemy healed!"
    

    def check(self):
        global npc_count
        if self.pok.hp == 0:
            player.game_state = "lose"
        if self.enemy.hp == 0:
            all_sprites.remove(current_npc)
            sprites.remove(current_npc)
            player.game_state = "win"
            npc_count -= 1


def is_pressed(key):
    for event in current_events:
        if event.type == pygame.KEYDOWN and event.key == key:
            current_events.remove(event)
            return True
    return False


def check_pokemon(name):
    for i, pok in enumerate(player.pokemons):
        if pok.name == name:
            return i
    return -1


def mining():
    screen.blit(images["brick_bg"], (0, 0))
    screen.blit(text_font.render(("Mine"), 1, "BLACK"), (10, 10))
    screen.blit(text_font.render((f"Coins: {player.coins}"), 1, "BLACK"), (430, 10))
    if is_pressed(pygame.K_SPACE):
        player.coins += 1
    
    screen.blit(text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))
    if is_pressed(pygame.K_q):
        player.game_state = "gameplay"


def gameplay():
    screen.fill((0, 180, 0))
    for e in all_sprites:
        screen.blit(e.image, camera.apply(e))

    inventory_icon = pygame.Surface((80, 80))
    inventory_icon.fill("BROWN")
    e_text = text_font.render("E", 1, "BLACK")
    inventory_icon.blit(e_text, (30, 20))
    screen.blit(inventory_icon, (0, 320))

    if len(player.pokemons) != 0:
        selected_name = player.pokemons[player.selected_pokemon_index].name
        screen.blit(select_pok_font.render(f"<- R | Selected Pokemon: {selected_name}| T -> ", 1, "BLACK"), (120, 370))
    if is_pressed(pygame.K_t):
        player.selected_pokemon_index += 1
        if player.selected_pokemon_index >= len(player.pokemons):
            player.selected_pokemon_index = 0
    if is_pressed(pygame.K_r):
        player.selected_pokemon_index -= 1
        if player.selected_pokemon_index < 0:
            player.selected_pokemon_index = len(player.pokemons) - 1

    player.update()
    camera.update()
    inventory.update()


def get_pokemon():
    screen.blit(images["brick_bg"], (0, 0))
    current_pokemon.draw(screen, 400, 100)
    screen.blit(text_font.render((f"{current_pokemon.probability}%"), 1, "BLACK"), (400, 170))
    screen.blit(text_font.render((f"F - use pokeball"), 1, "BLACK"), (50, 300))
    screen.blit(text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if is_pressed(pygame.K_f):
        player.pokeballs -= 1
        random_number = random.randint(1, 100)
        if random_number <= current_pokemon.probability:
            pokemon_index = check_pokemon(current_pokemon.name)
            if pokemon_index == -1:
                player.pokemons.append(copy.copy(current_pokemon))
            else:
                player.pokemons[pokemon_index].lvl += 1
                player.pokemons[pokemon_index].level_render()
            player.game_state = "success_pokemon"
        else:
            player.game_state = "fail_pokemon"
    
    if is_pressed(pygame.K_q):
        player.game_state = "gameplay"
    

def success_pokemon():
    screen.blit(images["brick_bg"], (0, 0))
    screen.blit(text_font.render((f"You got a pokemon!"), 1, "BLACK"), (150, 180))
    screen.blit(text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if is_pressed(pygame.K_q):
        player.game_state = "gameplay"


def fail_pokemon():
    screen.blit(images["brick_bg"], (0, 0))
    screen.blit(text_font.render((f"The pokemon ran away!"), 1, "BLACK"), (150, 180))
    screen.blit(text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if is_pressed(pygame.K_q):
        player.game_state = "gameplay"


def fight():
    current_fight.render()
    current_fight.fight()


def win():
    screen.blit(images["brick_bg"], (0, 0))
    screen.blit(text_font.render((f"You win!"), 1, "BLACK"), (150, 180))
    screen.blit(text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if is_pressed(pygame.K_q):
        player.game_state = "gameplay"


def lose():
    screen.blit(images["brick_bg"], (0, 0))
    screen.blit(text_font.render((f"You lose!"), 1, "BLACK"), (150, 180))
    screen.blit(text_font.render((f"Q - exit"), 1, "BLACK"), (50, 350))

    if is_pressed(pygame.K_q):
        player.game_state = "gameplay"


def init_pokemons():
    pokemon_list = levels[level_index][1]
    global pokemons
    pokemons = []
    for pokemon in pokemon_list:
        current_image = transform_image(pygame.image.load(pokemon[1]), 70, 70)
        current_pokemon = Pokemon(current_image, pokemon[0], pokemon[2], pokemon[3], pokemon[4])
        pokemons.append(current_pokemon)


def init_game():
    level = levels[level_index][0]
    global total_level_height, total_level_height, camera, npc_count
    total_level_width = len(level[0]) * 32
    total_level_height = len(level) * 32
    camera = Camera(Camera.camera_configure, total_level_width, total_level_height)

    for sprite in all_sprites:
        sprite.kill()
    sprites.clear()
    x = y = 0
    ground = Ground(0, 0)
    sprites.append(ground)
    for row in level:
        for col in row:
            if col == " ":
                random_number = random.randint(1, 100)
                if random_number <= 2:
                    rock = Rock(x, y, images[f"rock_{random_number}"])
                    sprites.insert(1, rock)
            
            if col == "-":
                block = Block(x, y)
                sprites.append(block)

            if col == "!":
                grass = Grass(x, y)
                sprites.append(grass)

            if col == "m":
                mine = Mine(x, y)
                sprites.append(mine)

            if col == "$":
                shop = Shop(x, y)
                sprites.append(shop)

            if col == "n":
                npc = NPC(x, y)
                sprites.append(npc)
                npc_count += 1

            if col == "e":
                exit_sprite = Exit(x, y)
                sprites.append(exit_sprite)

            x += PL_WIDTH
        y += PL_HEIGHT
        x = 0
    for sprite in sprites:
        all_sprites.add(sprite)
    all_sprites.add(player)


def transform_image(img, width, height):
    return pygame.transform.scale(img, (width, height))

images = {
    "grass": transform_image(pygame.image.load("./images/grass.png"), 2400, 1600),
    "brick": transform_image(pygame.image.load("./images/brick.png"), 32, 32),
    "tall_grass": pygame.image.load("./images/tall_grass.png"),
    "shop": pygame.image.load("./images/shop.png"),
    "mine": transform_image(pygame.image.load("./images/mine.png"), 96, 96),
    "rock_1": transform_image(pygame.image.load("./images/rock_1.png"), 24, 16),
    "rock_2": transform_image(pygame.image.load("./images/rock_2.png"), 12, 8),
    "player_left_1": transform_image(pygame.image.load("./images/player_left_1.png"), 25, 45),
    "player_left_2": transform_image(pygame.image.load("./images/player_left_2.png"), 25, 45),
    "player_left_3": transform_image(pygame.image.load("./images/player_left_3.png"), 25, 45),
    "player_right_1": transform_image(pygame.image.load("./images/player_right_1.png"), 25, 45),
    "player_right_2": transform_image(pygame.image.load("./images/player_right_2.png"), 25, 45),
    "player_right_3": transform_image(pygame.image.load("./images/player_right_3.png"), 25, 45),
    "brick_bg": transform_image(pygame.image.load("images/brick_bg.png"), 600, 400),
    "npc": transform_image(pygame.image.load("images/npc.png"), 32, 32),
    "exit": transform_image(pygame.image.load("images/exit.png"), 64, 64)
}


player = Player()
inventory = Inventory()
all_sprites = pygame.sprite.Group()
sprites = []
pokemons = []
current_events = []
current_pokemon = None
current_fight = None
current_npc = None
level_index = 0
npc_count = 0
dmg_tick = 0
msg_tick = 0
move_tick = 0
move_index = 0


with open("./levels.json") as levels_file:
    levels = json.load(levels_file)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 400))
total_level_width = 32
total_level_height = 32
camera = Camera(Camera.camera_configure, total_level_width, total_level_height)
def main():
    init_game()
    init_pokemons()
    run = True
    while run:
        global current_events
        current_events = pygame.event.get()
        if player.game_state == "gameplay":
            gameplay()
        elif player.game_state == "mining":
            mining()
        elif player.game_state == "get_pokemon":
            get_pokemon()
        elif player.game_state == "success_pokemon":
            success_pokemon()
        elif player.game_state == "fail_pokemon":
            fail_pokemon()
        elif player.game_state == "fight":
            fight()
        elif player.game_state == "win":
            win()
        elif player.game_state == "lose":
            lose()
        else:
            run = False
        
        global msg_tick
        msg_tick += 1

        for event in current_events:
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()