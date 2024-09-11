import pygame

class UI:
  def __init__(self, surface):

    self.display_surface = surface

    self.coin = pygame.image.load('Graphics/Coin/1.png').convert_alpha()
    self.coin = pygame.transform.scale(self.coin, (20, 20))
    self.coin_rect = self.coin.get_rect(topleft = (380, 15))
    self.font = pygame.font.Font('Font/ARCADECLASSIC.ttf', 28)

    self.start_time = pygame.time.get_ticks()
    self.clock = pygame.time.Clock()

  def show_coins(self, amount):
    self.display_surface.blit(self.coin, self.coin_rect)
    coin_amount_surf = self.font.render(f'x{amount:02d}', False, 'white')
    self.display_surface.blit(coin_amount_surf, (400, 10))
    

  def show_time(self):
    elapsed_time = pygame.time.get_ticks() - self.start_time
    elapsed_seconds = elapsed_time // 1000
    time_text = f'Time: {elapsed_seconds // 60:02d}:{elapsed_seconds % 60:02d}'
    time_surf = self.font.render(time_text, False, 'white')
    self.display_surface.blit(time_surf, (630, 10))
    

  def show_score(self, score):
    mario = self.font.render('MARIO', False, 'white')
    self.display_surface.blit(mario, (20, 10))
    score_surf = self.font.render(f'{score:05d}', False, 'white')
    self.display_surface.blit(score_surf, (20, 30))

  def show_level(self, current_level):
    world = self.font.render('WORLD', False, 'white')
    self.display_surface.blit(world, (410, 10))
    score_surf = self.font.render(f'01_{current_level:2d}', False, 'white')
    self.display_surface.blit(score_surf, (410, 30))
  