


import pygame, sys
from settings import *
from level import Level
from game_data import level_0

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Super Mario")

level = Level(screen, level_0, 5000)

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('Font/ARCADECLASSIC.ttf', 40)
        self.options = ["Choose   Level", "Settings", "Exit"]
        self.selected_option = 0
        self.bg_img = pygame.image.load('Graphics/Decorations/Menu.png')
        self.mario = pygame.image.load('Graphics/Mario/Idle/idle.png')
        self.rect = self.mario.get_rect(bottomleft = (100, 550))



    def draw(self):
        self.screen.fill("#63adff")
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.mario, self.rect)
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                label = self.font.render(option, True, (255, 0, 0))
            else:
                label = self.font.render(option, True, (255, 255, 255))
            self.screen.blit(label, (screen_width // 2 - label.get_width() // 2, screen_height // 2 + 110 + i * 40))
        

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            pygame.time.wait(150)
        elif keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            pygame.time.wait(150)
        elif keys[pygame.K_RETURN]:
            if self.selected_option == 0:
                return "overworld"
            elif self.selected_option == 1:
                return "settings"
            elif self.selected_option == 2:
                return "exit"
        return None
    
class Levels:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('Font/ARCADECLASSIC.ttf', 40)
        self.options = ["Choose   Level", "Settings", "Exit"]
        self.selected_option = 0
        self.bg_img = pygame.image.load('Graphics/Decorations/Menu.png')
        self.mario = pygame.image.load('Graphics/Mario/Idle/idle.png')
        self.rect = self.mario.get_rect(bottomleft = (100, 550))

    def draw(self):
        self.screen.fill("#63adff")
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.mario, self.rect)


def main(screen):
    clock = pygame.time.Clock()  
    run = True
    in_menu = True
    menu = Menu(screen)
    level_menu = Levels(screen)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        if in_menu:
            menu.draw()
            action = menu.handle_input()
            if action == "start_game":
                in_menu = False
            elif action == "settings":
                # Implement settings logic here
                pass
            elif action == "exit":
                run = False
                pygame.quit()
                sys.exit()
        else:
            screen.fill("#63adff")
            level.run()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main(screen)
