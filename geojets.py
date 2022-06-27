import pygame as py
from sys import exit
import math
from settings import *

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
        self.speed = 3

    def move(self):
        # pressed = py.key.get_pressed()
        # if pressed[py.K_a] or pressed[py.K_LEFT]:
        #      += self.speed
        # if pressed[py.K_d] or pressed[py.K_RIGHT]:
        #      -= self.speed
        # if pressed[py.K_w] or pressed[py.K_UP]:
        #      += self.speed
        # if pressed[py.K_s] or pressed[py.K_DOWN]:
        #      -= self.speed
        pass

    def rotate(self):
        mX, mY = py.mouse.get_pos()
        angleRad = math.atan2(self.rect.centery - mY, mX - self.rect.centerx)
        angleDeg = math.degrees(angleRad) - 90
        self.image = py.transform.rotate(self.img, angleDeg)
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))

    def update(self):
        self.move()
        self.rotate()

class Camera(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load(self.file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

py.init()
screen = py.display.set_mode((HEIGHT, WIDTH))
geojets_icon = py.image.load('images/globe.png').convert_alpha()
py.display.set_icon(geojets_icon)
py.display.set_caption('Geo Jets!')
py.mouse.set_visible(False)
clock = py.time.Clock()
game_active = True

player = py.sprite.GroupSingle()
player.add(Player())
cursor = py.sprite.GroupSingle()
cursor.add(Cursor())

while game_active:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()

    screen.fill(BGCOLOR)
    player.draw(screen)
    player.update()
    cursor.draw(screen)
    cursor.update()


    py.display.update()
    clock.tick(FPS)
