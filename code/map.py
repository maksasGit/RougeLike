import random
import sys

import pygame
import screeninfo

from settings import *
from timer import Timer

class Map():
    def __init__(self, groups):
        self.groups = groups
        self.size = 100
        self.map = [[0 for c in range(self.size)] for r in range(self.size)]
        self.setup()
        self.brick_size = 100
        self.create()


    def get_brick(self, x , y):
        if x >= 0 and x < self.size and y >= 0 and y < self.size:
            return self.map[x][y]
        else:
            return 0

    def setup(self):
        for x in range(self.size):
            for y in range(self.size):
                self.map[x][y] = random.randint(0,1)
        for x in range(self.size):
            for y in range(self.size):
                result = 0
                result += self.get_brick(x + 1 , y)
                result += self.get_brick(x - 1 , y)
                result += self.get_brick(x , y + 1)
                result += self.get_brick(x , y - 1)
                if result == 4:
                    self.map[x][y] = 1
        for x in range(self.size):
            for y in range(self.size):
                result = 0
                result += self.get_brick(x + 1 , y)
                result += self.get_brick(x - 1 , y)
                result += self.get_brick(x , y + 1)
                result += self.get_brick(x , y - 1)
                if result <= 2 and self.map[x][y] == 1:
                    if random.randint(0, 1) == 1:
                        self.map[x][y] = 0
        for x in range(self.size):
            for y in range(self.size):
                result = 0
                result += self.get_brick(x + 1 , y)
                result += self.get_brick(x - 1 , y)
                result += self.get_brick(x , y + 1)
                result += self.get_brick(x , y - 1)
                if result == 0 and self.map[x][y] == 1:
                        self.map[x][y] = 0


    def create(self):
        bricks = []
        for x  in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 1:
                    bricks.append(Brick(x*self.brick_size , y *self.brick_size, self.groups , self.brick_size))


    def create_brick(self ,x , y ,groups, size):
        return Brick(x , y , groups , size)

class Brick(pygame.sprite.Sprite):
    def __init__(self, x , y , groups, brick_size):
        super().__init__(groups)
        self.brick_size = brick_size
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load('C:/Users/imaks/PycharmProjects/pythonProject1/graphics/objects/tree_medium.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.hitbox = self.rect.copy()



    def update(self, dt):
        pass
