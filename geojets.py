import pygame as py
from sys import exit
import math
from settings import *

class Background(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load('images/bg/13.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.x = 2000
        self.y = 2000

    def update(self, px, py):
        self.rect.topleft = ((px - self.x) * -1, (py - self.y) * -1)

class Cursor(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load('images/cursor.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = py.mouse.get_pos()

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = py.image.load('images/jet.png').convert_alpha()
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

py.init()
screen = py.display.set_mode((HEIGHT, WIDTH))
geojets_icon = py.image.load('images/globe.png').convert_alpha()
py.display.set_icon(geojets_icon)
py.display.set_caption('Geo Jets!')
py.mouse.set_visible(False)
clock = py.time.Clock()
game_active = True
font = py.font.SysFont("Arial" , 18 , bold = True)

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
    background.draw(screen)
    background.update(player.sprite.x, player.sprite.y)
    player.draw(screen)
    player.update()
    cursor.draw(screen)
    cursor.update()
    fps_counter()                                                       #####

    py.display.update()
    clock.tick(FPS)
