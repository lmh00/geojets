import pygame as py
from sys import exit
import math
from init import*
from settings import *

class Background(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bg13
        self.rect = self.image.get_rect()
        self.rect.topleft = ((2500 - 2000) * -1, (2500 - 2000) * -1)

class Cursor(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cursor_icon
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = py.mouse.get_pos()

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = jet_icon
        self.image = self.img
        self.rect = self.image.get_rect(center = (HEIGHT / 2, WIDTH / 2))
        self.x = 2500
        self.y = 2500
        self.speed = 3

    def move(self):
        pressed = py.key.get_pressed()
        if pressed[py.K_a] or pressed[py.K_LEFT]:
            self.x -= self.speed
        if pressed[py.K_d] or pressed[py.K_RIGHT]:
            self.x += self.speed
        if pressed[py.K_w] or pressed[py.K_UP]:
            self.y -= self.speed
        if pressed[py.K_s] or pressed[py.K_DOWN]:
            self.y += self.speed

    def rotate(self):
        mX, mY = py.mouse.get_pos()
        angleRad = math.atan2(self.rect.centery - mY, mX - self.rect.centerx)
        angleDeg = math.degrees(angleRad) - 90
        self.image = py.transform.rotate(self.img, angleDeg)
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))

    def update(self):
        self.move()
        self.rotate()

background = py.sprite.GroupSingle()
background.add(Background())
player = py.sprite.GroupSingle()
player.add(Player())
cursor = py.sprite.GroupSingle()
cursor.add(Cursor())

while game_active:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()

    def fps_counter():                                                  #####
        fps = str(int(clock.get_fps()))                                 #####
        fps_t = font.render(fps , 1, py.Color("RED"))                   #####
        screen.blit(fps_t,(0,0))                                        #####

    screen.fill(BGCOLOR)
    background.update()
    background.draw(screen)
    player.update()
    player.draw(screen)
    cursor.update()
    cursor.draw(screen)
    fps_counter()                                                       #####

    py.display.update()
    clock.tick(FPS)
