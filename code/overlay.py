import pygame
from settings import *

class Overlay:
	def __init__(self,player):

		# general setup
		self.display_surface = pygame.display.get_surface()
		self.player = player
		self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

		self.display_surface = pygame.display.get_surface()
		self.player = player

		# imports
		overlay_path = 'C:/Users/imaks/PycharmProjects/pythonProject1/graphics/overlay/'
		self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in
						   player.tools}

	def display(self):

		# if self.player.damage > 0:
		# 	text_surf = self.font.render(f'{self.player.damage}', False, 'white')
		# 	text_rect = text_surf.get_rect(midbottom=(self.player.pos.x , self.player.pos.y - 30))
		# 	self.display_surface.blit(text_surf, text_rect)
		# 	self.player.HP -= self.player.damage
		# 	self.player.damage = 0
		# tool
		tool_surf = self.tools_surf[self.player.selected_tool]
		tool_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
		self.display_surface.blit(tool_surf, tool_rect)


		if self.player.health_points < 0:
			self.player.health_points = 0
		HP_surf = pygame.Surface((self.player.health_points * 3, 30))
		HP_surf.fill('brown')
		HP_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['HP'])
		self.display_surface.blit(HP_surf, HP_rect)
