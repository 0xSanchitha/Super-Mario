import pygame
from settings import screen_height, screen_width
from game_data import levels

class Level:
  def __init__(self, current_level, surface, create_overworld):
    
    self.current_level = current_level
    self.display_surface = surface

    level_data = levels[current_level]
    level_content = level_data['content']
    self.new_max_level = level_data['unlock']
    self.create_overworld = create_overworld

    self.font = pygame.font.Font(None, 40)
    self.text_surf = self.font.render(level_content, True, 'white')
    self.text_rect = self.text_surf.get_rect(center = (screen_width / 2, screen_height / 2))

  def input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
      self.create_overworld(self.current_level, self.new_max_level)
    if keys[pygame.K_ESCAPE]:
      self.create_overworld(self.current_level, 0)


  def run(self):
    self.input()
    self.display_surface.blit(self.text_surf, self.text_rect)