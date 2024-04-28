import pygame
import random
import sys
pygame.init()
WIDTH, HEIGHT = 900, 800
FPS = 60
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goblin Hunter")
background = pygame.image.load('data/images/background.png').convert_alpha()
background = pygame.transform.scale(background, (900, 700))
title_background = pygame.transform.scale(background.copy(), (900, 800))

def quit():
    sys.exit()
moving = [True, True]
turn = [True]

class Player:
    player_font = pygame.font.SysFont('Arial', 30)
    large_font = pygame.font.SysFont('Arial', 64)
    def __init__(self, name, health, shd):
        self.name = name
        self.health = health
        self.shd = shd
        self.damage = 2
        self.play = pygame.image.load('data/images/Player.png').convert_alpha()
        self.attacker = pygame.image.load('data/images/Attack.png').convert_alpha()
        self.inventories = pygame.image.load('data/images/Inventory.png').convert_alpha()
        self.attack_hitbox = pygame.Rect(205, 660, 150, 110)
        self.hearts = pygame.image.load('data/images/Heart.png').convert_alpha()
        self.hearts = pygame.transform.scale2x(self.hearts)
        self.shield = pygame.transform.scale_by(pygame.image.load('data/images/Shield.png').convert_alpha(), 1.2)
        self.sword = pygame.transform.scale_by(pygame.image.load('data/images/Sword.png'), 1.5)
        self.upgrades = pygame.transform.scale_by(pygame.image.load('data/images/Upgrade.png'), 20)
        self.rect1 = [190, 660]
        self.rect = [300, 400]
        self.rect2 = [360, 660]
        self.text = self.player_font.render(f"{self.health}", False, (255, 255, 255))
        self.inventory_hitbox = pygame.Rect(WIDTH//2-95, 660, 210, 110)
        self.reduction = pygame.transform.scale_by(pygame.image.load('data/images/Shield.png'), 0.25)
        self.shd_text = self.player_font.render(f"{self.shd}", False, (255, 255, 255))

    def move(self):
        if self.rect[0] == 100:
            moving[0] = False
        elif self.rect[0] == 250:
            moving[0] = True
        if moving[0]:
            self.rect[0] -= 2
        else:
            self.rect[0] += 2

    def attack(self, health):
        if health <= self.damage:
            return health
        else:
            self.attacks = random.randint(1, self.damage)
        return self.attacks

    def upgrade(self, num):
        heart = pygame.Rect(40, 300, 260, 260)
        shield = pygame.Rect(heart.x+270, 300, 260, 260)
        dmg = pygame.Rect(shield.x + 270, 300, 260, 260)
        hp_gain = int(round(2 ** (num//2)))
        print(hp_gain)
        shield_gain = random.randint(1, 3)
        dmg_gain = random.randint(1, 4)
        health_text = self.player_font.render(f"You will heal {hp_gain}", False, (255, 0, 0))
        shield_text = self.player_font.render(f"You will gain {shield_gain} shield", False, (0, 255, 0))
        dmg_text = self.player_font.render(f"You will gain {dmg_gain} damage", False, (0, 0, 255))

        run = True
        while run:
            mouse = pygame.mouse.get_pos()
            clock.tick(FPS)
            window.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse1 = pygame.Rect(mouse[0], mouse[1], 10, 10)
                    if mouse1.colliderect(heart):
                        self.health += hp_gain
                        self.remove_health()
                        run = False
                    if mouse1.colliderect(shield):
                        self.shd += shield_gain
                        self.shield_checker()
                        run = False
                    if mouse1.colliderect(dmg):
                        self.damage += dmg_gain
                        run = False
            pygame.draw.rect(window, (255, 0, 0), heart, 1)
            pygame.draw.rect(window, (0, 255, 0), shield, 1)
            pygame.draw.rect(window, (0, 0, 255), dmg, 1)
            window.blit(health_text, (100, 600))
            window.blit(shield_text, (300, 600))
            window.blit(dmg_text, (600, 600))
            window.blit(self.hearts, (-200, 70))
            window.blit(self.shield, (225, 270))
            window.blit(self.sword, (460, 140))
            window.blit(self.upgrades, (WIDTH//2-self.upgrades.get_width()//2, 0))
            pygame.display.update()

    def shield_checker(self):
        self.shd_text = self.player_font.render(f"{self.shd}", False, (255, 255, 255))

    def inventory(self):
        self.pot = pygame.transform.scale_by(pygame.image.load('data/images/Potion.png').convert_alpha(), 19.5)
        self.l_pot = pygame.transform.scale_by(pygame.image.load('data/images/Large pot.png').convert_alpha(), 14)
        hp_text = self.player_font.render("+5 HP", False, (255, 255, 255))
        large_hptext = self.player_font.render("+10 HP", False, (255, 255, 255))
        button1 = pygame.Rect(0, 2, 300, 300)
        button2 = pygame.Rect(310, 2, 300, 300)
        run = True
        while run:
            clock.tick(FPS)
            window.fill((70, 42, 42))
            pygame.draw.rect(window, (255, 255, 255), button1, 1)
            pygame.draw.rect(window, (255, 255, 255), button2, 1)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse1 = pygame.Rect(mouse[0], mouse[1], 10, 10)
                    if mouse1.colliderect(button1):
                        self.health += 5
                        turn[0] = False
                        self.remove_health()
                        run = False
                    if mouse1.colliderect(button2):
                        self.health += 10
                        turn[0] = False
                        self.remove_health()
                        run = False
            window.blit(hp_text, (100, 300))
            window.blit(large_hptext, (350, 300))
            window.blit(self.pot, (-120, -150))
            window.blit(self.l_pot, (249, -78))
            pygame.display.update()

    def game_won(self):
        run = True
        self.winningtext = self.large_font.render("YOU WIN!", False, (255, 255, 255))
        while run:
            window.fill('blue')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
            window.blit(self.winningtext, (WIDTH//2-self.winningtext.get_width()//2, HEIGHT//2-self.winningtext.get_height()//2))
            pygame.display.update()



    def remove_health(self):
        if self.health >= 0:
            self.text = self.player_font.render(f"{self.health}", False, (255, 255, 255))
        if self.health <= 0:
            self.dead = self.large_font.render("You are Dead", False, (255, 255, 255))
            self.space = self.player_font.render("Press Space to Try Again", False, (255, 255, 255))
            run = True
            while run:
                clock.tick(FPS)
                window.fill('black')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        quit()
                    '''if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            run = False
                window.blit(self.space, (WIDTH//2 - self.space.get_width()//2, 600))'''
                window.blit(self.dead, (WIDTH//2 - self.dead.get_width()//2, HEIGHT//2 - self.dead.get_height()//2))
                pygame.display.update()

    def bar(self):
        pygame.draw.rect(window, (255, 0, 0), (WIDTH//2-235, 610, self.health * 10, 30))
        '''pygame.draw.rect(window, (1, 50, 32), ())'''
        window.blit(self.text, (WIDTH//2+200, 605))

    def draw(self):
        window.fill('black')
        self.move()
        self.shield_checker()
        window.blit(background, (0, 0))
        window.blit(self.shd_text, (180, 380))
        window.blit(self.play, self.rect)
        pygame.draw.rect(window, (255, 0, 0), self.attack_hitbox, 1)
        window.blit(self.attacker, self.rect1)
        pygame.draw.rect(window, (255, 255, 255), (WIDTH//2-500//2, 600, 500, 180), 1)
        pygame.draw.rect(window, (255, 0, 255), self.inventory_hitbox, 1)
        window.blit(self.inventories, self.rect2)
        window.blit(self.reduction, (200, 370))
        self.bar()

    def title_screen(self):
        run = True
        title_text = self.large_font.render("Goblin Hunter", True, (255, 255, 255))
        text = self.player_font.render("Press Space to Continue", False, (255, 255, 255))
        while run:
            window.fill('black')
            window.blit(title_background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False
            window.blit(title_text, (WIDTH//2-title_text.get_width()//2, HEIGHT//2-title_text.get_height()//2))
            window.blit(text, (WIDTH//2-text.get_width()//2, 500))
            pygame.display.update()



class Enemy:
    enemy_font = pygame.font.SysFont('Arial', 30)
    large_font = pygame.font.SysFont('Arial', 100)

    def __init__(self, name, health, etc):
        self.naming = name
        self.name = self.enemy_font.render(f"{name}", False, (255, 255, 255))
        self.health = health
        self.etc = etc
        self.goblin = pygame.image.load('data/images/goblins.png').convert_alpha()
        self.rect = [500, 400]
        self.text = self.enemy_font.render(f"{self.health}", False, (255, 255, 255))

    def remove_health(self):
        self.text = self.enemy_font.render(f"{self.health}", False, (255, 255, 255))

    def move(self):
        if self.rect[0] == 500:
            moving[1] = False
        elif self.rect[0] == 650:
            moving[1] = True
        if moving[1]:
            self.rect[0] -= 2
        else:
            self.rect[0] += 2

    def attack(self, health):
        if self.naming == "George":
            self.number = random.randint(1, 3)
        elif self.naming == "Rob":
            self.number = random.randint(1, 8)
        elif self.naming == "Benny":
            self.number = random.randint(1, 10)
        elif self.naming == "Arthur":
            self.number = random.randint(5, 20)
        else:
            self.number = random.randint(10, 50)
        return self.number

    def hp_checker(self):
        if self.health <= 0:
            return True
        else:
            return False

    def bar(self):
        self.remove_health()
        pygame.draw.rect(window, (255, 0, 0), (WIDTH // 2 - self.health*50 // 2 + 200, 400, self.health * 50, 30))
        window.blit(self.name, (WIDTH // 2 - self.name.get_width()//2 + 200, 360))
        window.blit(self.text, (WIDTH // 2 + 320, 400))

    def draw(self):
        self.hp_checker()
        self.move()
        window.blit(self.goblin, self.rect)
        self.bar()

def game():
    run = True
    player = Player("Nathaniel", 20, 1)
    stage_enemies = [Enemy("George", 4, 4), Enemy("Rob", 5, 4), Enemy("George", 4, 4), Enemy("George", 4, 4), Enemy("Rob", 5, 4), Enemy("Benny", 8, 4)
        , Enemy("Rob", 5, 4), Enemy("Benny", 8, 4), Enemy("Benny", 8, 4), Enemy("Benny", 8, 4), Enemy("Benny", 8, 4), Enemy("Arthur", 12, 4),Enemy("Arthur", 10, 4), Enemy("Arthur", 15, 4), Enemy("Arthur", 12, 4),
                     Enemy("Goliath", 30, 4)]
    font = pygame.font.Font(None, 100)
    orig_surf = font.render('Players Turn', True, (255, 255, 255))
    txt_surf = orig_surf.copy()
    # This surface is used to adjust the alpha of the txt_surf.
    alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
    alpha = 255  # The current alpha value of the surface.
    timer = 0
    numb_of_enemies_killed = 0
    val = False
    player.title_screen()
    while run:
        mouse = pygame.mouse.get_pos()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and turn[0]:
                mouserect = pygame.Rect(mouse[0], mouse[1], 10, 10)
                if mouserect.colliderect(player.inventory_hitbox):
                    player.inventory()
                    if not turn[0]:
                        orig_surf = font.render("Enemy Turn", True, (255, 255, 255))
                        alpha = 255
                        timer = 120
                if mouserect.colliderect(player.attack_hitbox):
                    stage_enemies[0].health -= player.attack(stage_enemies[0].health)
                    if stage_enemies[0].health <= 0:
                        del stage_enemies[0]
                        numb_of_enemies_killed += 1
                    turn[0] = False
                    orig_surf = font.render("Enemy Turn", True, (255, 255, 255))
                    alpha = 255
                    timer = 120
        if not turn[0]:
            if timer <= 0 or val:
                player.health -= stage_enemies[0].attack(player.health) // (player.shd+1)
                player.remove_health()
                turn[0] = True
                orig_surf = font.render('Players Turn', True, (255, 255, 255))
                alpha = 255
            timer -= 1
        if alpha > 0:
            # Reduce alpha each frame, but make sure it doesn't get below 0.
            alpha = max(alpha-1.2, 0)
            txt_surf = orig_surf.copy()  # Don't modify the original text surf.
            # Fill alpha_surf with this color to set its alpha value.
            alpha_surf.fill((255, 255, 255, alpha))
            # To make the text surface transparent, blit the transparent
            # alpha_surf onto it with the BLEND_RGBA_MULT flag.
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if numb_of_enemies_killed == 3:
            player.upgrade(numb_of_enemies_killed)
            numb_of_enemies_killed -= 3
        player.draw()
        if len(stage_enemies) <= 0:
            player.game_won()
        stage_enemies[0].draw()
        screen.blit(txt_surf, (WIDTH//2-txt_surf.get_width()//2, 200))
        if stage_enemies[0].hp_checker():
            del stage_enemies[0]
        pygame.display.flip()

    pygame.quit()
    quit()


if __name__ == "__main__":
    game()