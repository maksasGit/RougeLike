import pygame

from support import *
from settings import *
from timer import Timer

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, enemy_collision_sprites , fruit_collision_sprites , map_collision_sprite, toggle_shop , start_menu_change_status):
		super().__init__(groups)
				# general setup
		self.import_assets()
		self.start_menu_change_status = start_menu_change_status
		self.map_collision_sprite = map_collision_sprite
		self.status = 'down_idle'
		self.frame_index = 0
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center=(pos))
		self.toggle_shop = toggle_shop
		self.need_hit = False

			# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 200
		self.strength = 35
		# health
		self.set_health_settings()
		self.set_level_settings()
		# collision
		self.hitbox = self.image.get_rect().inflate(-120 , -60)
		self.damage_area_image = pygame.Surface((40 , 64))
		self.damage_area_image_rect = self.damage_area_image.get_rect()
		self.damage_area_image_rect.top = self.hitbox.bottom
		self.damage = self.strength
		self.enemy_collision_sprites = enemy_collision_sprites
		self.fruit_collision_sprites = fruit_collision_sprites


		self.tools = ['hoe' , 'axe']
		self.tool_index = 1
		self.selected_tool = self.tools[self.tool_index]


		self.timers = {
			'tool use': Timer(350),
			'tool switch': Timer(200),
			'seed use': Timer(350),
			'seed switch': Timer(200),
		}

	def update_strength(self):
		self.damage = self.strength

	def set_level_settings(self):
		self.expirience = 0
		self.expirience_need = 40
		self.level_points = 0

	def set_health_settings(self):
		self.health_points_limit = 100;
		self.health_points = 100

	def import_assets(self):
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

		for animation in self.animations.keys():
			full_path = 'C:/Users/imaks/PycharmProjects/pythonProject1/graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

	def level_up(self):
		if self.expirience >= self.expirience_need:
			self.expirience -= self.expirience_need
			self.expirience_need *= 1.3
			self.level_points += 1

	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	def get_status(self):

		# idle
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'

		# tool use
		if self.timers['tool use'].active:
			self.status = self.status.split('_')[0] + '_' + self.selected_tool


	def input(self):
		keys = pygame.key.get_pressed()
		#print(self.timers['tool use'].active)
		if not self.timers['tool use'].active:
			if keys[pygame.K_e]:
				self.timers['tool use'].activate()
				self.frame_index = 0
				self.need_hit = True
						
			if keys[pygame.K_w]:
				self.direction.y = -1
				self.status = 'up'
				self.damage_area_image = pygame.Surface((53, 40))
				self.damage_area_image_rect = self.damage_area_image.get_rect()
				self.damage_area_image_rect.bottomleft = self.hitbox.topleft
				self.damage_area_image_rect.bottomright = self.hitbox.topright
			elif keys[pygame.K_s]:
				self.direction.y = 1
				self.status = 'down'
				self.damage_area_image = pygame.Surface((53, 40))
				self.damage_area_image_rect = self.damage_area_image.get_rect()
				self.damage_area_image_rect.topleft = self.hitbox.bottomleft
				self.damage_area_image_rect.topright = self.hitbox.bottomright
			else:
				self.direction.y = 0

			if keys[pygame.K_d]:
				self.direction.x = 1
				self.status = 'right'
				self.damage_area_image = pygame.Surface((40, 64))
				self.damage_area_image_rect = self.damage_area_image.get_rect()
				self.damage_area_image_rect.topleft = self.hitbox.topright
				self.damage_area_image_rect.bottomleft = self.hitbox.bottomright
			elif keys[pygame.K_a]:
				self.direction.x = -1
				self.status = 'left'
				self.damage_area_image = pygame.Surface((40, 64))
				self.damage_area_image_rect = self.damage_area_image.get_rect()
				self.damage_area_image_rect.topright = self.hitbox.topleft
				self.damage_area_image_rect.bottomright = self.hitbox.bottomleft
			else:
				self.direction.x = 0
		else:
			if self.timers['tool use'].active and int(self.frame_index) == 1 and self.need_hit:
				self.need_hit = False
				for enemy in self.enemy_collision_sprites.sprites():
					if enemy.rect.colliderect(self.damage_area_image_rect):
						enemy.damage(self.damage)
				for brick in self.map_collision_sprite.sprites():
					if brick.rect.colliderect(self.damage_area_image_rect):
						brick.kill()

	def animate(self, dt):
		self.frame_index += 4 * dt
		if self.frame_index >= len(self.animations[self.status]):
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)]

	def collision(self, direction):
		for sprite in self.enemy_collision_sprites.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == 'horizontal':
						if self.direction.x > 0: # moving right
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: # moving left
							self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx

					if direction == 'vertical':
						if self.direction.y > 0: # moving down
							self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0: # moving up
							self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery
		for sprite in self.map_collision_sprite.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == 'horizontal':
						if self.direction.x > 0: # moving right
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: # moving left
							self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx

					if direction == 'vertical':
						if self.direction.y > 0: # moving down
							self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0: # moving up
							self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery


	def move(self,dt):
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

	def get_fruit(self):
		self.health_points += 10

	def check_death(self):
		if self.health_points <= 0:
			self.start_menu_change_status()

	def update(self, dt):
		self.input()
		self.get_status()
		self.level_up()
		self.move(dt)
		self.update_timers()
		self.check_death()
		self.animate(dt)
