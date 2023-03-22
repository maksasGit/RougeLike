import pygame
import random

import settings
from settings import *
from player import Player
from enemy import Enemy
from overlay import Overlay



class Apple(pygame.sprite.Sprite):
    def __init__(self, pos, groups , player_collision_sprites, player):
        super().__init__(groups)
        self.image = pygame.image.load('C:/Users/imaks/PycharmProjects/pythonProject1/graphics/overlay/tomato.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30 , 30))
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.player_collision_sprites = player_collision_sprites
        self.player = player
        self.hitbox = self.rect.copy()

    def collision(self):
        for player in self.player_collision_sprites.sprites():
            if self.hitbox.colliderect(player.hitbox):
                self.player.get_fruit()
                self.kill()


    def update(self, dt):
        self.collision()


