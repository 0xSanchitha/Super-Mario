import pygame
from Main import main

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
        self.rect = self.mario.get_rect(bottomleft = (100, 550))

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

menu = Menu(screen)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action = menu.handle_input()
    if action == "Exit":
        running = False

    if action == "Choose   Level":
        main(screen)

    menu.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
