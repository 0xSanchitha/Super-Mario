import pygame
from support import import_csv_layout, import_cut_graphics
from settings import *
from tiles import Tile, StaticTile, Cloud, AnimatedTile,Coin
from enemy import Enemy
from player import Player, Mushroomx2
from game_data import levels
from particleeffect import ParticleEffect
import random

pygame.init()
pygame.mixer.init()

class Level:
    def __init__(self, current_level, surface, create_overworld, change_coin, change_score, change_health):
        self.display_surface = surface
        self.world_shift = 0
        self.speed = 5
        self.level_width = 5000
        self.coin_spawned = False

        self.create_overworld = create_overworld
        self.current_level = current_level

        level_data = levels[self.current_level]

        self.new_max_level = level_data['unlock']

        player_layout = import_csv_layout(level_data['Player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        self.all_sprites = pygame.sprite.Group()

        self.change_coins = change_coin
        self.change_score = change_score
        self.change_health = change_health
        

        self.kill_sprite = pygame.sprite.Group()

        self.mushroomx2_sprite = pygame.sprite.Group()

        terrain_layout = import_csv_layout(level_data['Terrain'])
        self.terrain_sprite = self.create_tile_group(terrain_layout, 'Terrain')

        random_box_layout = import_csv_layout(level_data['Random_Box'])
        self.random_box_sprite = self.create_tile_group(random_box_layout, 'Random_Box')

        Mushroom_layout = import_csv_layout(level_data['Mushroom'])
        self.Mushroom_sprite = self.create_tile_group(Mushroom_layout, 'Mushroom')

        Cloud_1_layout = import_csv_layout(level_data['Cloud 1'])
        self.Cloud_1_sprite = self.create_tile_group(Cloud_1_layout, 'Cloud 1')

        Cloud_2_layout = import_csv_layout(level_data['Cloud 2'])
        self.Cloud_2_sprite = self.create_tile_group(Cloud_2_layout, 'Cloud 2')

        Mountain_layout = import_csv_layout(level_data['Mountain'])
        self.Mountain_sprite = self.create_tile_group(Mountain_layout, 'Mountain')

        Bush_layout = import_csv_layout(level_data['Bush'])
        self.Bush_sprite = self.create_tile_group(Bush_layout, 'Bush')

        Castel_layout = import_csv_layout(level_data['Castel'])
        self.Castel_sprite = self.create_tile_group(Castel_layout, 'Castel')

        Coin_layout = import_csv_layout(level_data['Coin'])
        self.Coin_sprite = self.create_tile_group(Coin_layout, 'Coin')

        Goomba_layout = import_csv_layout(level_data['Goomba'])
        self.Goomba_sprite = self.create_tile_group(Goomba_layout, 'Goomba')

        Goomba_Barrier_layout = import_csv_layout(level_data['Goomba Barrier'])
        self.Goomba_Barrier_sprite = self.create_tile_group(Goomba_Barrier_layout, 'Goomba Barrier')

        Koopa_layout = import_csv_layout(level_data['Koopa'])
        self.Koopa_sprite = self.create_tile_group(Koopa_layout, 'Koopa')

        Koopa_Barrier_layout = import_csv_layout(level_data['Koopa Barrier'])
        self.Koopa_Barrier_sprite = self.create_tile_group(Koopa_Barrier_layout, 'Koopa Barrier')

        hammer_bro_layout = import_csv_layout(level_data['Hammer Bro'])
        self.hammer_bro_sprite = self.create_tile_group(hammer_bro_layout, 'Hammer Bro')

        hammer_bro_Barrier_layout = import_csv_layout(level_data['Hammer Bro Barrier'])
        self.hammer_bro_Barrier_sprite = self.create_tile_group(hammer_bro_Barrier_layout, 'Hammer Bro Barrier')

        Boo_layout = import_csv_layout(level_data['Boo'])
        self.Boo_sprite = self.create_tile_group(Boo_layout, 'Boo')

        Boo_Barrier_layout = import_csv_layout(level_data['Boo Barrier'])
        self.Boo_Barrier_sprite = self.create_tile_group(Boo_Barrier_layout, 'Boo Barrier')

        self.coin_sound = pygame.mixer.Sound("./sfx/coin.ogg")
        self.powerup = pygame.mixer.Sound('./sfx/powerup.ogg')
        self.powerup_appear = pygame.mixer.Sound('./sfx/powerup_appears.ogg')
        self.stomp = pygame.mixer.Sound("./sfx/stomp.ogg")
        self.death = pygame.mixer.Sound("./sfx/death.wav")
        self.bump = pygame.mixer.Sound("./sfx/bump.ogg")
        self.brick_bump = pygame.mixer.Sound("./sfx/brick-bump.ogg")

        self.win = pygame.mixer.Sound("./sfx/win.mp3")

    def create_tile_group(self, layout, type):
        sprite_Group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'Terrain':
                        terrain_tile_list = import_cut_graphics('Graphics/Tiles/Tileset.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "Random_Box":
                        random_images = ['Graphics/Tiles/Random Box.png', 'Graphics/Tiles/block.png']  # List of image paths
                        random_image = random.choice(random_images)  # Choose a random image from the list
                        sprite = Cloud(tile_size, x, y, random_image)

                    if type == "Mushroom":
                        sprite = Cloud(tile_size, x, y, 'Graphics/Tiles/Random Box.png')

                    if type == "Cloud 1":
                        sprite = Cloud(tile_size, x, y, 'Graphics/Decorations/Cloud 1.png')

                    if type == "Cloud 2":
                        sprite = Cloud(tile_size, x, y, 'Graphics/Decorations/Cloud 2.png')

                    if type == "Mountain":
                        sprite = Cloud(tile_size, x, y, 'Graphics/Decorations/Mountain.png')

                    if type == "Bush":
                        sprite = Cloud(tile_size, x, y, 'Graphics/Decorations/Bushesh.png')

                    if type == "Castel":
                        sprite = Cloud(tile_size, x, y, 'Graphics/Decorations/Castel.png')

                    if type == "Coin":
                        sprite = Coin(tile_size, x, y, 'Graphics/Coin/Coins')

                    if type == "Goomba":
                        sprite = Enemy(tile_size, x, y, 'Graphics/Goomba/run')

                    if type == "Goomba Barrier":
                        sprite = Tile(tile_size, x, y)

                    if type == "Koopa":
                        sprite = Enemy(tile_size, x, y, 'Graphics/Koopa/run')

                    if type == "Koopa Barrier":
                        sprite = Tile(tile_size, x, y)

                    if type == "Hammer Bro":
                        sprite = Enemy(tile_size, x, y, 'Graphics/Hammer Bro/run')

                    if type == "Hammer Bro Barrier":
                        sprite = Tile(tile_size, x, y)

                    if type == "Boo":
                        sprite = Enemy(tile_size, x, y, 'Graphics/Boo/chase')

                    if type == "Boo Barrier":
                        sprite = Tile(tile_size, x, y)

                    sprite_Group.add(sprite)

        return sprite_Group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), change_health)
                    self.player.add(sprite)

                if val == "1":
                    End_surface = pygame.image.load('Graphics/Decorations/end.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, End_surface)
                    self.goal.add(sprite)

    def enemy_collusion_revers(self):
        for goomba in self.Goomba_sprite.sprites():
            if pygame.sprite.spritecollide(goomba, self.Goomba_Barrier_sprite, False):
                goomba.reverse()

        for koopa in self.Koopa_sprite.sprites():
            if pygame.sprite.spritecollide(koopa, self.Koopa_Barrier_sprite, False):
                koopa.reverse()

        for hammer_bro in self.hammer_bro_sprite.sprites():
            if pygame.sprite.spritecollide(hammer_bro, self.hammer_bro_Barrier_sprite, False):
                hammer_bro.reverse()

        for Boo in self.Boo_sprite.sprites():
            if pygame.sprite.spritecollide(Boo, self.Boo_Barrier_sprite, False):
                Boo.reverse()

    def horizontal_movement_collusion(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * self.speed
        collidable_sprite = self.terrain_sprite.sprites() + self.random_box_sprite.sprites() + self.Mushroom_sprite.sprites()
        for sprite in collidable_sprite:
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
        collidable_sprite = self.terrain_sprite.sprites() + self.random_box_sprite.sprites() + self.Mushroom_sprite.sprites()
        for sprite in collidable_sprite:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 1
                    player.on_ceiling = True

                

                    if sprite in self.random_box_sprite:
                        self.create_coin(sprite.rect.x, sprite.rect.y - tile_size)
                        self.change_coins(1)
                        self.change_score(100)
                        
                        new_image = pygame.image.load('Graphics/Tiles/Tile.png').convert_alpha()
                        sprite.image = pygame.transform.scale(new_image, (tile_size, tile_size))
                        self.brick_bump.play()

                    if sprite in self.Mushroom_sprite:
                        new_image = pygame.image.load('Graphics/Tiles/Tile.png').convert_alpha()
                        sprite.image = pygame.transform.scale(new_image, (tile_size, tile_size))

                        mushroomx2 = Mushroomx2((sprite.rect.x, sprite.rect.y - 20))
                        self.mushroomx2_sprite.add(mushroomx2)
                        self.powerup_appear.play()
                        self.bump.play()
                        

                            

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False


    def create_coin(self, x, y):
        coin = Coin(tile_size, x, y, 'Graphics/Coin/Coins')
        self.Coin_sprite.add(coin)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0 and self.world_shift < 0:
            self.world_shift = 0
            self.speed = 5
        elif player_x > self.level_width - screen_width / 4 and direction_x > 0 and self.world_shift > -self.level_width:
            self.world_shift = 0
            self.speed = 5
        elif player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 5
            self.speed = 0
        elif player_x > screen_width - screen_width / 4 and direction_x > 0:
            self.world_shift = -5
            self.speed = 0
        else:
            self.world_shift = 0
            self.speed = 5

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.death.play()
            pygame.time.delay(2500)
            self.create_overworld(self.current_level, self.current_level)
            self.player.sprite.health = 1
            self.player.sprite.bonus_points = 0

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.player.sprite.health = 1
            self.player.sprite.bonus_points = 0
            self.win.play()
            if self.new_max_level <= 3:
                pygame.time.delay(2500)
                self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collision(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.Coin_sprite, True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(1)
                self.change_score(100)
                self.coin_sound.play()

    def check_enemy_collison(self):
        goomba_collision = pygame.sprite.spritecollide(self.player.sprite, self.Goomba_sprite, False)

        if goomba_collision:
            for goomba in goomba_collision:
                goomba_center = goomba.rect.centery
                goomba_top = goomba.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if goomba_top < player_bottom < goomba_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    goomba_dead_sprite = ParticleEffect(goomba.rect.center, 'goomba kill')
                    self.kill_sprite.add(goomba_dead_sprite)
                    self.stomp.play()
                    self.change_score(100)
                    goomba.kill()

                else:
                    self.player.sprite.get_damage()
                    if not self.player.sprite.bonus_points == 0:
                        self.player.sprite.bonus_points -= 1


        Koopa_collision = pygame.sprite.spritecollide(self.player.sprite, self.Koopa_sprite, False)

        if Koopa_collision:
            for Koopa in Koopa_collision:
                Koopa_center = Koopa.rect.centery
                Koopa_top = Koopa.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if Koopa_top < player_bottom < Koopa_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    koopa_hide_sprite = ParticleEffect((Koopa.rect.centerx, Koopa.rect.centery + 20), 'koopa hide')
                    self.kill_sprite.add(koopa_hide_sprite)
                    self.stomp.play()
                    self.change_score(100)
                    Koopa.kill()

                else:
                    self.player.sprite.get_damage()
                    self.player.sprite.get_damage()
                    if not self.player.sprite.bonus_points == 0:
                        self.player.sprite.bonus_points -= 1

        Boo_collision = pygame.sprite.spritecollide(self.player.sprite, self.Boo_sprite, False)

        if Boo_collision:
            for Boo in Boo_collision:
                Boo_center = Boo.rect.centery
                Boo_top = Boo.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if Boo_top < player_bottom < Boo_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    self.stomp.play()
                    self.change_score(100)
                    Boo.kill()

                else:
                    self.player.sprite.get_damage()
                    self.player.sprite.get_damage()
                    if not self.player.sprite.bonus_points == 0:
                        self.player.sprite.bonus_points -= 1

        hammer_bro_collision = pygame.sprite.spritecollide(self.player.sprite, self.hammer_bro_sprite, False)

        if hammer_bro_collision:
            for hammer_bro in hammer_bro_collision:
                hammer_bro_center = hammer_bro.rect.centery
                hammer_bro_top = hammer_bro.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if hammer_bro_top < player_bottom < hammer_bro_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    self.stomp.play()
                    self.change_score(100)
                    hammer_bro.kill()

                else:
                    self.player.sprite.get_damage()
                    self.player.sprite.get_damage()
                    if not self.player.sprite.bonus_points == 0:
                        self.player.sprite.bonus_points -= 1

    def mushroomx2_vertical_movement_collision(self):
        for mushroom in self.mushroomx2_sprite.sprites():
            mushroom.apply_gravity()
            collidable_sprite = self.terrain_sprite.sprites() + self.random_box_sprite.sprites() + self.Mushroom_sprite.sprites()
            for sprite in collidable_sprite:
                if sprite.rect.colliderect(mushroom.rect):
                    if mushroom.direction.y > 0:
                        mushroom.rect.bottom = sprite.rect.top
                        mushroom.direction.y = 0
                        mushroom.on_ground = True
                    elif mushroom.direction.y < 0:
                        mushroom.rect.top = sprite.rect.bottom
                        mushroom.direction.y = 1

            if mushroom.on_ground and mushroom.direction.y != 0:
                mushroom.on_ground = False

    def mushroomx2_collision_revers(self):
        for mushroom in self.mushroomx2_sprite.sprites():
            # Check for collision with terrain
            for sprite in self.terrain_sprite.sprites():
                if mushroom.rect.colliderect(sprite.rect):
                    if mushroom.direction.x > 0:  # Moving right
                        mushroom.rect.right = sprite.rect.left
                    elif mushroom.direction.x < 0:  # Moving left
                        mushroom.rect.left = sprite.rect.right
                    mushroom.reverse()

            # Check for collision with other boundaries
            if mushroom.rect.left <= 0 or mushroom.rect.right >= self.level_width:
                mushroom.reverse()

    def check_player_near_boo(self):
        player = self.player.sprite
        if len(self.Boo_sprite.sprites()) > 0:
            boo = self.Boo_sprite.sprites()[0]  # Assuming there's only one Boo sprite
            boo_rect = boo.rect
            boo_rect_around = pygame.Rect(boo.rect.left - 100, boo.rect.top - 100, 400, 400)  # Adjust dimensions as needed

        # Check if the player's rectangle collides with Boo's rectangle
            if player.rect.colliderect(boo_rect_around):
                if player.rect.x < boo_rect.x:
                    boo_rect.x -= 1  # Move Boo left
                    boo.image = pygame.transform.flip(boo.image, True, False)
                elif player.rect.x > boo_rect.x:
                    boo_rect.x += 1  # Move Boo right
                    boo.image = pygame.transform.flip(boo.image, False, False)
                if player.rect.y < boo.rect.y:
                    boo_rect.y -= 1  # Move Boo up
                elif player.rect.y > boo_rect.y:
                    boo.rect.y += 1  # Move Boo down

        else:
            pass
                    

    def run(self):
        self.Cloud_1_sprite.update(self.world_shift)
        self.Cloud_1_sprite.draw(self.display_surface)

        self.Cloud_2_sprite.update(self.world_shift)
        self.Cloud_2_sprite.draw(self.display_surface)

        self.Mountain_sprite.update(self.world_shift)
        self.Mountain_sprite.draw(self.display_surface)

        self.Bush_sprite.update(self.world_shift)
        self.Bush_sprite.draw(self.display_surface)

        self.Castel_sprite.update(self.world_shift)
        self.Castel_sprite.draw(self.display_surface)

        self.terrain_sprite.update(self.world_shift)
        self.terrain_sprite.draw(self.display_surface)

        self.random_box_sprite.update(self.world_shift)
        self.random_box_sprite.draw(self.display_surface)

        self.Mushroom_sprite.update(self.world_shift)
        self.Mushroom_sprite.draw(self.display_surface)

        self.Coin_sprite.update(self.world_shift)
        self.Coin_sprite.draw(self.display_surface)

        self.Goomba_sprite.update(self.world_shift)
        self.Goomba_Barrier_sprite.update(self.world_shift)
        self.Goomba_sprite.draw(self.display_surface)

        self.Koopa_sprite.update(self.world_shift)
        self.Koopa_Barrier_sprite.update(self.world_shift)
        self.Koopa_sprite.draw(self.display_surface)

        self.hammer_bro_sprite.update(self.world_shift)
        self.hammer_bro_Barrier_sprite.update(self.world_shift)
        self.hammer_bro_sprite.draw(self.display_surface)

        self.mushroomx2_sprite.update(self.world_shift)
        self.mushroomx2_sprite.draw(self.display_surface)

        self.Boo_sprite.update(self.world_shift)
        self.Boo_Barrier_sprite.update(self.world_shift)
        self.Boo_sprite.draw(self.display_surface)


        self.mushroomx2_collision_revers()
        self.mushroomx2_vertical_movement_collision()
        self.enemy_collusion_revers()

        self.player.update()
        self.horizontal_movement_collusion()
        self.vertical_movement_collusion()
        self.scroll_x()
        self.player.draw(self.display_surface)

        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_coin_collision()

        self.kill_sprite.update(self.world_shift)
        self.kill_sprite.draw(self.display_surface)

        self.check_enemy_collison()
        
        self.check_player_near_boo()

        # Handle collision
        player_mushroom_collision = pygame.sprite.spritecollide(self.player.sprite, self.mushroomx2_sprite, True)

        # Handle collision
        if player_mushroom_collision:
            # Assuming Mushroomx2 provides some value, let's say 'bonus_points'
            for mushroom in player_mushroom_collision:
                bonus_points = mushroom.bonus_points  # Accessing the bonus points directly
                self.player.sprite.bonus_points += 1
                self.change_health(1)
                self.change_score(100)

                self.powerup.play()