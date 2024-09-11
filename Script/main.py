import pygame, sys
from settings import *
from level import Level

pygame.init()

screen = pygame.display.set_mode((SCCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario")

level = Level(screen, level_map)

def main(screen):
  clock = pygame.time.Clock()
  fps = 60
  run = True

  while run:
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
        sys.exit()

    
    screen.fill('#63adff')
    level.run()
    clock.tick(fps)
    pygame.display.update()

if __name__ == "__main__":
  main(screen)
