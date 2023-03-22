import pygame,sys
from  settings import *
from level import Level
from start_menu import StartMenu
from map import Map

class Game:
    def __init__(self):
        pygame.init();
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Rogalik")
        self.clock = pygame.time.Clock()
        self.start_menu_status = True
        self.level = None
        self.start_menu = StartMenu(self.screen , self.start_menu_change_status)

    def start_menu_change_status(self):
        self.start_menu_status = not self.start_menu_status

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            if self.start_menu_status:
                self.level = None
                self.start_menu.update()
            else:
                if self.level == None:
                    self.level = Level(self.start_menu_change_status)
                self.level.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()