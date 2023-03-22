import math
import random

import pygame
from settings import *
from player import Player
from timer import Timer
from support import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, player):
        super().__init__(groups)
        # general setup
        self.type = ENEMY_CHARACTERISTICKS[random.randint(0 , len(ENEMY_CHARACTERISTICKS)-1)]
        #print(ENEMY_CHARACTERISTICKS[random.randint(0 , len(ENEMY_CHARACTERISTICKS)-1)])
        self.import_assets()
        self.status = 'idle'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(pos))
        self.player = player
        self.should_dead = True
        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed  = 100
        self.health_points = 200
        self.timers = {
            'tool use': Timer(1450),
            'tool switch': Timer(200),
            'seed use': Timer(350),
            'seed switch': Timer(200),
            'damage': Timer(300),
            'death': Timer(300),
        }
        # collision
        self.hitbox = self.rect.copy()
        self.collision_sprites = collision_sprites

    def input(self):
        if not self.timers['tool use'].active:
            if self.find_distance() < 63:
                self.timers['tool use'].activate()
                #rewrite player damage
                self.player.health_points -= 3
            elif self.find_distance() < 200:
                if self.pos.x > self.player.pos.x:
                    self.status = 'idle'
                    self.direction.x = -1
                if self.pos.x < self.player.pos.x:
                    self.status = 'idle'
                    self.direction.x = 1
                if self.pos.y > self.player.pos.y:
                    self.status = 'idle'
                    self.direction.y = -1
                if self.pos.y < self.player.pos.y:
                    self.status = 'idle'
                    self.direction.y = 1
            else:
                self.direction.x = 0
                self.direction.y = 0
        else:
            self.direction.x = 0
            self.direction.y = 0


    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'death': [], 'damage': [], 'attack':[] , 'idle':[]}

        for animation in self.animations.keys():
            full_path = 'C:/Users/imaks/PycharmProjects/pythonProject1/graphics/Slimes/'+self.type+'Slime/' + animation
            self.animations[animation] = import_folder(full_path)


    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def get_status(self):
        if not self.timers['damage'].active:
            if self.direction.magnitude() == 0:
                self.status = 'idle'

            if self.timers['tool use'].active:
                self.status = 'idle'



    def animate(self, dt):
        #print(self.frame_index)
        self.frame_index += (10 * dt)
       # print(str(self.frame_index) + " " + str(len(self.animations[self.status])))
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (50, 50))

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def find_distance(self):
        #rewrite AI
        distance = ((self.pos.x - self.player.pos.x) * (self.pos.x - self.player.pos.x)) + ((self.pos.y - self.player.pos.y) * (self.pos.y - self.player.pos.y))
        distance = math.sqrt(distance)
        return distance

    def damage(self , damaged):
        self.health_points -= damaged
        self.status = 'damage'
        self.timers['damage'].activate()
        #show damage as number
        #change hp bar

    def check_death(self):
        if self.health_points <= 0:
            self.status = 'death'
            if self.should_dead:
                self.timers['death'].activate()
                self.should_dead = False
            if not self.timers['death'].active:
                self.player.expirience += 10
                self.kill()

    def update(self, dt):
        self.update_timers()
        if self.status != 'death':
            self.input()
            self.get_status()
            self.move(dt)
        self.update_timers()
        self.check_death()
        self.animate(dt)
