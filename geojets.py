import pygame as py
from sys import exit
import math

# Classes
class Background():
    def update(self, px, py):
        screen.blit(map, (0, 0), (px, py, WIDTH, HEIGHT))

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
        self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self.x = 0
        self.y = 0
        self.speed = 10

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

# Settings
WIDTH = 1200
HEIGHT = 800
FPS = 60
BGCOLOR = 'skyblue'

# Init
py.init()
screen = py.display.set_mode((WIDTH, HEIGHT))
font = py.font.SysFont("Arial" , 18 , bold = True)
clock = py.time.Clock()
py.mouse.set_visible(False)
py.display.set_caption('Geo Jets!')
game_active = True

# Background Images
map = py.image.load('images/bg/eq_earth.png').convert_alpha()
cursor_icon = py.image.load('images/cursor.png').convert_alpha()
jet_icon = py.image.load('images/jet.png').convert_alpha()
logo_icon = py.image.load('images/globe.png').convert_alpha()
py.display.set_icon(logo_icon)

#Groups
background = Background()
player = py.sprite.GroupSingle()
player.add(Player())
cursor = py.sprite.GroupSingle()
cursor.add(Cursor())

# Game loop
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
    background.update(player.sprite.x, player.sprite.y)
    player.update()
    player.draw(screen)
    cursor.update()
    cursor.draw(screen)
    fps_counter()                                                       #####

    py.display.update()
    clock.tick(FPS)
