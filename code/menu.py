import sys

import pygame
import screeninfo

from settings import *
from timer import Timer

class Menu:
	def __init__(self, player, toggle_menu ):

		# general setup
		self.player = player
		self.toggle_menu = toggle_menu
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)
		self.status = False
		# options
		self.width = 400
		self.space = 10
		self.padding = 8
		self.pos = 0
		self.maks_pos = 3

		# entries
		self.setup()

		# movement
		self.index = 0
		self.timer = Timer(200)




	def display_level_points(self):
		text_surf = self.font.render(f"Level point(s): {self.player.level_points}", False, 'Black')
		text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 270))
		self.display_surface.blit(text_surf, text_rect)

	def display_expirience(self):
		x = SCREEN_WIDTH / 2
		y = SCREEN_HEIGHT / 2 - 220
		text_surf = self.font.render(f"{int(self.player.expirience)}/{int(self.player.expirience_need)}", False, 'black')
		text_rect = text_surf.get_rect(center=(x + 200, y))
		exp_box_surf = pygame.Surface((300, 30))
		exp_box_rect = exp_box_surf.get_rect(center=(x, y))
		exp_surf = pygame.Surface((300/self.player.expirience_need*self.player.expirience, 24))
		exp_rect = exp_surf.get_rect(topleft=(x-147, y-12))
		pygame.draw.rect(self.display_surface, 'black', exp_box_rect, 0, 3)
		pygame.draw.rect(self.display_surface, 'lightblue', exp_rect, 0, 3)
		self.display_surface.blit(text_surf, text_rect)

	def display_skill_box(self , x , y , lable, color):
		skill_box_surf = pygame.Surface((500 , 75))
		skill_box_rect = skill_box_surf.get_rect(center=(x , y))
		pygame.draw.rect(self.display_surface, color, skill_box_rect, 0, 17)
		text_surf = self.font.render(f'{lable}', False, 'White')
		text_rect = text_surf.get_rect(center=(x, y))
		self.display_surface.blit(text_surf, text_rect)

	def show_skill_points(self):
		text_surf = self.font.render(f"Speed: {int(self.player.speed)}", False, 'darkred')
		text_rect = text_surf.get_rect(topleft=(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 100))
		self.display_surface.blit(text_surf, text_rect)
		text_surf = self.font.render(f"Heath: {int(self.player.health_points_limit)}", False, 'darkred')
		text_rect = text_surf.get_rect(topleft=(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 140))
		self.display_surface.blit(text_surf, text_rect)
		text_surf = self.font.render(f"Strength: {int(self.player.strength)}", False, 'darkred')
		text_rect = text_surf.get_rect(topleft=(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 + 180))
		self.display_surface.blit(text_surf, text_rect)

	def display_skills(self):
		skills = ['speed' , 'health' , 'strength' , 'exit']
		it = 0
		for label in skills:
			color = 'Black'
			if it == self.pos:
				color = 'darkgray'
			if label != 'exit':
				x = SCREEN_WIDTH / 2
				y = SCREEN_HEIGHT / 2 - (150) + (it*100)
				self.display_skill_box(x , y , label , color)
				it+=1
			else:
				self.display_skill_box(SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2 + 250 , label, color)




	def display_menu(self):
		menu_surf = pygame.Surface((700,600))
		menu_rect = menu_surf.get_rect(center = (SCREEN_WIDTH / 2,SCREEN_HEIGHT/2))
		pygame.draw.rect(self.display_surface,'White',menu_rect,0,17)
		self.display_level_points()
		self.display_expirience()
		self.display_skills()
		self.show_skill_points()


	def setup(self):

		# create the text surfaces
		self.text_surfs = []
		self.total_height = 0



		self.total_height += (len(self.text_surfs) - 1) * self.space
		self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
		self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2,self.menu_top,self.width,self.total_height)

		# buy / sell text surface
		self.buy_text = self.font.render('buy',False,'Black')
		self.sell_text =  self.font.render('sell',False,'Black')

	def change_button(self, direction):
		if direction == 'up':
			self.pos -= 1
		else:
			self.pos += 1
		if self.pos > self.maks_pos:
			self.pos = 0
		if self.pos < 0:
			self.pos = self.maks_pos
		self.timer.activate()
		#self.change_button_sound.play()


	def activate_button(self):
		self.timer.activate()
		#print(str(self.player.speed) + " " + str(self.player.health_points_limit) + " " + str(self.player.strength))
		if self.pos == 3:
			pygame.QUIT
			sys.exit()
		if self.player.level_points!=0:
			if self.pos == 0:
				self.player.level_points-=1
				self.player.speed *= 1.1
			if self.pos == 1:
				self.player.level_points -= 1
				self.player.health_points_limit*=1.1
			if self.pos == 2:
				self.player.level_points -= 1
				self.player.strength *= 0.9
				self.player.update_strength()

	def input(self):
		keys = pygame.key.get_pressed()
		if not self.timer.active:
			if keys[pygame.K_ESCAPE]:
				self.toggle_menu()
				self.status = not self.status
				self.timer.activate()

		if not self.timer.active:
			if keys[pygame.K_UP]:
				self.change_button('up')

			if keys[pygame.K_DOWN]:
				self.change_button('down')

			if keys[pygame.K_RETURN]:
				self.activate_button()



	def show_entry(self, text_surf, amount, top, selected):

		# background
		bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + (self.padding * 2))
		pygame.draw.rect(self.display_surface, 'White',bg_rect, 0, 4)

		# text
		text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20,bg_rect.centery))
		self.display_surface.blit(text_surf, text_rect)

		# amount
		amount_surf = self.font.render(str(amount), False, 'Black')
		amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20,bg_rect.centery))
		self.display_surface.blit(amount_surf, amount_rect)

		# selected
		if selected:
			pygame.draw.rect(self.display_surface,'black',bg_rect,4,4)
			if self.index <= self.sell_border: # sell
				pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
				self.display_surface.blit(self.sell_text,pos_rect)
			else: # buy
				pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
				self.display_surface.blit(self.buy_text,pos_rect)


	def background(self):
		background_surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
		color = (40,40,40)
		background_surf.fill(color)
		self.display_surface.blit(background_surf , (0,0) , special_flags=pygame.BLEND_RGB_MULT)


	def update(self):
		self.input()
		if self.status:
			self.background()
			self.display_menu()
		self.timer.update()