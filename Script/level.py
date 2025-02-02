import pygame
from tile import Tile
from player import Player
from settings import *

class Level:
  def __init__(self, surface, level_data):
    self.display_surface = surface
    self.setup_level(level_data)

    self.word_shift = 0
    self.speed = 5
    self.current_x = 0

  def setup_level(self, layout):
    self.tiles = pygame.sprite.Group()
    self.player = pygame.sprite.GroupSingle()

    for row_index, row in enumerate(layout):
      for col_index, cell in enumerate(row):
        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE
        if cell == 'X':
          tile = Tile((x, y), TILE_SIZE)
          self.tiles.add(tile)
        
        if cell == "P":
          player_sprite = Player((x, y))
          self.player.add(player_sprite)
  
  def scroll_x(self):
      player = self.player.sprite
      player_x = player.rect.centerx
      direction_x = player.direction.x

      if player_x < SCCREEN_WIDTH / 4 and direction_x < 0:
        self.word_shift = 5
        self.speed = 0

      elif player_x > SCCREEN_WIDTH - (SCCREEN_WIDTH / 4) and direction_x > 0:
        self.word_shift = -5
        self.speed = 0

      else:
        self.word_shift = 0
        self.speed = 5

  def horizontal_movement_collusion(self):

    player = self.player.sprite
    player.rect.x += player.direction.x * self.speed

    for sprite in self.tiles.sprites():
      if sprite.rect.colliderect(player.rect):
        if player.direction.x < 0:
          player.rect.left = sprite.rect.right
          player.on_left = True
          self.current_x = player.rect.left

        elif player.direction.x > 0:
          player.rect.right = sprite.rect.left
          player.on_right = True
          self.current_x = player.rect.right

    if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
      player.on_left = False

    if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
      player.on_right = False

  def vertical_movement_collusion(self):
    player = self.player.sprite
    player.apply_gravity()

    for sprite in self.tiles.sprites():
      if sprite.rect.colliderect(player.rect):
        if player.direction.y > 0:
          player.rect.bottom = sprite.rect.top
          player.direction.y = 0
          player.on_ground = True

        elif player.direction.y < 0:
          player.rect.top = sprite.rect.bottom
          player.direction.y = 1
          player.on_ceiling = True

    if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
      player.on_ground = False

    if player.on_ceiling and player.direction.y > 0:
      player.on_ceiling = False

  def run(self):
    self.tiles.update(self.word_shift)
    self.tiles.draw(self.display_surface)

    self.player.update(self.speed)
    self.horizontal_movement_collusion()
    self.vertical_movement_collusion()
    self.player.draw(self.display_surface)

    self.scroll_x()