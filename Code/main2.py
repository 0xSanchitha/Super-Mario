import pygame, sys
from settings import *
from overworld import Overworld
from levels2 import Level


class Game:
  def __init__(self):
    self.max_level = 0
    self.overworld = Overworld(0, self.max_level, screen, self.create_level)
    self.status = "overworld"

  def create_level(self, current_level):
    self.level = Level(current_level, screen, self.create_overworld)
    self.status = 'level'

  def create_overworld(self, current_level, new_max_level):
    if new_max_level > self.max_level:
      self.max_level = new_max_level
    self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
    self.status = 'overworld'

  def run(self):
    if self.status == 'overworld':
      self.overworld.run()

    else:
      self.level.run()

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Super Mario")

game = Game()


def main(screen):
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

if __name__ == "__main__":
  main(screen)