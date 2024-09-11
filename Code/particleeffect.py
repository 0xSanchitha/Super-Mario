import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5

        if type == 'goomba kill':
            self.frames = import_folder('Graphics/Goomba/Dead')

        if type == 'koopa hide':
            self.frames = import_folder('Graphics/koopa/Hide')
            self.animation_speed = 0.003

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
