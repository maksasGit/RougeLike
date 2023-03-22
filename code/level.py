import pygame
import random

import settings
from settings import *
from player import Player
from enemy import Enemy
from overlay import Overlay
from subjects import Apple
from menu import Menu
from start_menu import StartMenu
from map import Map

class Level:
	def __init__(self, start_menu_status):
		self.start_menu_status = start_menu_status
		# get the display surface
		self.display_surface = pygame.display.get_surface()
		self.all_sprites = CameraGroup()
		self.enemy_collision_sprites = pygame.sprite.Group()
		self.player_collision_sprites = pygame.sprite.Group()
		self.fruts_collision_sprites = pygame.sprite.Group()
		self.map_collision_sprite = pygame.sprite.Group()
		self.test_collision_sprite = pygame.sprite.Group()
		self.setup()
		self.overlay = Overlay(self.player)

		# shop
		self.menu = Menu(self.player, self.toggle_shop)
		self.shop_active = False




	def check_test_surf(self , x , y , size):
		brik = self.map.create_brick(x , y , [self.all_sprites , self.test_collision_sprite] , size)
		#print(self.test_collision_sprite)
		#print(self.map_collision_sprite)
		#print(pygame.sprite.groupcollide(self.test_collision_sprite , self.map_collision_sprite, False , False))
		if pygame.sprite.groupcollide(self.test_collision_sprite , self.map_collision_sprite , False, False):
			brik.remove([self.all_sprites , self.test_collision_sprite])
			return True
		else:
			brik.remove([self.all_sprites, self.test_collision_sprite])
			return False

	def setup(self):
		self.map = Map([self.all_sprites , self.map_collision_sprite])
		x = random.randint(0, self.map.size * self.map.brick_size)
		y = random.randint(0, self.map.size * self.map.brick_size)
		# print(self.check_test_surf(x , y))
		while self.check_test_surf(x, y, 80):
			x = random.randint(0, self.map.size * self.map.brick_size)
			y = random.randint(0, self.map.size * self.map.brick_size)
		self.player = Player((x , y), [self.all_sprites , self.player_collision_sprites] , self.enemy_collision_sprites , self.fruts_collision_sprites , self.map_collision_sprite, self.toggle_shop, self.start_menu_status)
		self.enemys = []
		for i in range(300):
			x = random.randint(0,self.map.size * self.map.brick_size)
			y = random.randint(0,self.map.size * self.map.brick_size)
			#print(self.check_test_surf(x , y))
			while self.check_test_surf(x,y , 50):
				x = random.randint(0, self.map.size * self.map.brick_size)
				y = random.randint(0, self.map.size * self.map.brick_size)
			self.enemys.append(Enemy((x, y), [self.all_sprites, self.enemy_collision_sprites], self.player_collision_sprites,self.player))
		self.fruts = []
		for i in range(100):
			x = random.randint(0, self.map.size * self.map.brick_size)
			y = random.randint(0, self.map.size * self.map.brick_size)
			while self.check_test_surf(x, y , 30):
				x = random.randint(0, self.map.size * self.map.brick_size)
				y = random.randint(0, self.map.size * self.map.brick_size)
			self.fruts.append( Apple((x, y), [self.all_sprites, self.fruts_collision_sprites] , self.player_collision_sprites , self.player))


	def toggle_shop(self):
		self.shop_active = not self.shop_active

	def run(self,dt):
		self.display_surface.fill('black')
		#pygame.draw.rect(self.display_surface ,'orange', self.player.hitbox)
		#for enemy in self.enemy_collision_sprites.sprites():
		#	pygame.draw.rect(self.display_surface ,'orange' , enemy.hitbox)
		#pygame.draw.rect(self.display_surface ,'blue', self.player.damage_area_image_rect)

		self.all_sprites.custom_draw(self.player)
		self.menu.update()
		if not self.shop_active:
				self.all_sprites.update(dt)
				self.overlay.display()



class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for sprite in self.sprites():
			offset_rect = sprite.rect.copy()
			offset_rect.center -= self.offset
			self.display_surface.blit(sprite.image, offset_rect)

			# # anaytics
			# if sprite == player:
			# 	pygame.draw.rect(self.display_surface,'red',offset_rect,5)
			# 	hitbox_rect = player.hitbox.copy()
			# 	hitbox_rect.center = offset_rect.center
			# 	pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
			# 	target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
