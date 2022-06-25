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
        self.jet = py.image.load('images/jet.png').convert_alpha()
        self.image = self.jet
        self.rect = self.image.get_rect(center = (HEIGHT / 2, WIDTH / 2))
        self.speed = 3

    def move(self):
        pressed = py.key.get_pressed()
        if pressed[py.K_a] or pressed[py.K_LEFT]:
            bg.sprite.rect.centerx += self.speed
        if pressed[py.K_d] or pressed[py.K_RIGHT]:
            bg.sprite.rect.centerx -= self.speed
        if pressed[py.K_w] or pressed[py.K_UP]:
            bg.sprite.rect.centery += self.speed
        if pressed[py.K_s] or pressed[py.K_DOWN]:
            bg.sprite.rect.centery -= self.speed

    def rotate(self):
        mX, mY = py.mouse.get_pos()
        angleRad = math.atan2(self.rect.centery - mY, mX - self.rect.centerx)
        angleDeg = math.degrees(angleRad) - 90
        self.image = py.transform.rotate(self.jet, angleDeg)
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))

    def update(self):
        self.move()
        self.rotate()

class Background(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = py.image.load('images/1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (0, 0))

    def render(self):
        if bg.sprite.rect.top > 0 and bg.sprite.rect.top < 251:
            self.image = py.image.load('images/1.png').convert_alpha()
        if bg.sprite.rect.top > 250 and bg.sprite.rect.top < 501:
            self.image = py.image.load('images/2.png').convert_alpha()
        if bg.sprite.rect.top > 500 and bg.sprite.rect.top < 751:
            self.image = py.image.load('images/3.png').convert_alpha()
        if bg.sprite.rect.top > 750 and bg.sprite.rect.top < 1001:
            self.image = py.image.load('images/4.png').convert_alpha()

    def update(self):
        self.render()

py.init()
screen = py.display.set_mode((HEIGHT, WIDTH))
geojets_icon = py.image.load('./images/globe.png').convert_alpha()
py.display.set_icon(geojets_icon)
py.display.set_caption('Geo Jets!')
py.mouse.set_visible(False)
clock = py.time.Clock()
game_active = True

bg = py.sprite.GroupSingle()
bg.add(Background())
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
    bg.draw(screen)
    bg.update()
    player.draw(screen)
    player.update()
    cursor.draw(screen)
    cursor.update()


    py.display.update()
    clock.tick(FPS)
