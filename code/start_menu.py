import sys

import pygame
from timer import Timer

class StartMenu():
    def __init__(self , screen , change_status):
        self.change_status = change_status
        self.screen = screen
        self.labels = ['start' , 'options' , 'exit']
        self.pos = 0
        self.maks_pos = 2
        self.timers = {
            'change_button': Timer(200)
        }
        self.change_button_sound = pygame.mixer.Sound('code\menu.mp3')
        self.change_button_sound.set_volume(1)


    def change_button(self, direction):
        if direction == 'up':
            self.pos-=1
        else:
            self.pos+=1
        if self.pos > self.maks_pos:
            self.pos = 0
        if self.pos < 0:
            self.pos = self.maks_pos
        self.timers['change_button'].activate()
        self.change_button_sound.play()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['change_button'].active:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.change_button("down")
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.change_button("up")
            if keys[pygame.K_RETURN]:
                self.button_pressed()


    def button_pressed(self):
        if self.pos == 0:
            self.change_status()
        if self.pos == 1:
            self.status = False
        if self.pos == 2:
            pygame.quit()
            sys.exit()

        pass


    def make_label(self, pos , text , color , size):
        font = pygame.font.Font('font/LycheeSoda.ttf', size)
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.midleft = (pos)
        self.screen.blit(text, textRect)

    def draw(self):
        self.screen.fill('black')
        self.make_label((100 ,100) , 'Rogalik' , 'white' , 150)
        for i in range(3):
            if (self.pos == i):
                self.make_label((600 , 400 + (i * 100)) , self.labels[i] , 'red' , 96)
            else:
                self.make_label((600, 400 + (i * 100)), self.labels[i], 'white', 96)
        self.make_label((1250 ,750) , 'Made by' , 'white' , 40)
        self.make_label((1250 ,800) , 'Maksim Ryshko' , 'white' , 40)


    def update(self):
        for timer in self.timers.values():
            timer.update()
        self.input()
        self.draw()
