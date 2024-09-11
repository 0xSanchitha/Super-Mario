import pygame
from support import import_folder
from math import sin
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, change_health):
        super().__init__()

        self.bonus_points = 0
        self.import_character_assets()
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['Idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -16
        self.status = 'Idle'
        self.facing_right = True

        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 400
        self.hurt_time = 0

        self.jump_sound = pygame.mixer.Sound("./sfx/small_jump.ogg")

    def update_bonus_points(self, bonus_points):
        self.bonus_points = bonus_points
        self.import_character_assets()

    def import_character_assets(self):
        if self.bonus_points > 0:
            character_path = 'Graphics/Big Mario/'
        else: 
            character_path = 'Graphics/Big Mario/'
        self.animations = {'Idle': [], 'Run': [], 'Jump': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            # print(f"Loaded {len(self.animations[animation])} frames for {animation} animation.")


    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.bonus_points > 0:
            image = pygame.transform.scale(image, (50, 100))
        else:
            image = pygame.transform.scale(image, (40, 50))
        if self.facing_right:
          self.image = image
        else:
          self.image = pygame.transform.flip(image, True, False)

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)

        else:
            self.image.set_alpha(255)

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)

        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)

        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)

        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)

        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False

        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
      
      if self.direction.y < 0:
        self.status = "Jump"

      elif self.direction.y > 1:
          self.status = "Jump"

      else:
          if self.direction.x != 0:
              self.status = "Run"

          else:
              self.status = "Idle"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_damage(self):
        if not self.invincible:
            self.change_health(-1)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()

            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.invincibility_timer()
        self.wave_value()

class Mushroomx2(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Graphics/Mushroom/Mushroom.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), 0)
        self.speed = 2
        self.gravity = 0.8
        self.direction.y = 0
        self.on_ground = False
        self.gravity_enabled = False
        self.bonus_points = 1
        

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def reverse(self):
        self.direction.x *= -1

    def update(self, x_shift):
        self.rect.x += (self.direction.x * self.speed) + x_shift
        self.apply_gravity()

        if self.rect.right >= 800:
            self.direction.x = -1
        elif self.rect.left <= 0:
            self.direction.x = 1


class Hammer(pygame.sprite.Sprite):
    def __init__(self, size, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self, world_shift):
        self.rect.x -= self.speed