import pygame
import sys
from settings import *
from level import Level
from game_data import level_0
from overworld import Overworld
from ui import UI

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Super Mario")

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('Font/ARCADECLASSIC.ttf', 40)
        self.options = ["Choose   Level", "Settings", "Exit"]
        self.selected_option = 0
        self.bg_img = pygame.image.load('Graphics/Decorations/Menu.png')
        self.mario = pygame.image.load('Graphics/Mario/Idle/idle.png')
        self.rect = self.mario.get_rect(bottomleft=(100, 550))

    def draw(self):
        self.screen.fill('#63adff')
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.mario, self.rect)
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_option else (255, 255, 255)
            label = self.font.render(option, True, color)
            x = screen_width // 2 - label.get_width() // 2
            y = screen_height // 2 + 110 + i * 40
            self.screen.blit(label, (x, y))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            pygame.time.wait(150)
        elif keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            pygame.time.wait(150)
        elif keys[pygame.K_RETURN]:
            return self.options[self.selected_option]
        return None

    def run_game(self):
        game = Game()
        clock = pygame.time.Clock()
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            screen.fill("#63adff")
            game.run()

            pygame.display.update()
            clock.tick(60)

class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./sfx/main_theme.ogg")
        pygame.mixer.music.play(-1)
        self.death = pygame.mixer.Sound("./sfx/death.wav")
        self.max_level = 0
        self.health = 1
        self.coins = 0
        self.score = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = "overworld"

        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_score, self.change_health)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def change_coins(self, amount):
        self.coins += amount

    def change_score(self, amount):
        self.score += amount

    def change_health(self, amount):
        self.health += amount

    def check_game_over(self):
        if self.health <= 0:
            self.death.play()
            pygame.time.delay(2500)
            self.health = 1
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = "overworld"

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()

        else:
            self.level.run()
            self.ui.show_coins(self.coins)
            self.ui.show_time()
            self.ui.show_score(self.score)
            self.check_game_over()

menu = Menu(screen)
game = Game()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.K_ESCAPE:
            game.status = 'overworld'
    action = menu.handle_input()
    if action == "Exit":
        running = False
    elif action == "Choose   Level":
        menu.run_game()

    menu.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
