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

    def move(self):
        self.rect.center = py.mouse.get_pos()

    def update(self):
        self.move()

class FPS_Counter():                                                    #####
    def update(self):                                                   #####
        fps = str(int(clock.get_fps()))                                 #####
        fps_t = font.render(fps , 1, py.Color("RED"))                   #####
        screen.blit(fps_t,(0,0))                                        #####

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = square_icon
        self.image = self.img
        self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self.x = 5000
        self.y = 5000
        self.angle = 0
        self.speed = 3

    def turn(self):
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

    def load(self):
        click = py.mouse.get_pressed(3)[0]
        if click:
            new_bullet = bullet.add(Bullet(self.x, self.y))
            bullets.append(new_bullet)

    def update(self):
        self.turn()
        self.rotate()
        self.load()

class Bullet(py.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img = bullet_icon
        self.image = self.img
        self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self.position = [x, y]
        self.speed = 1

    def move(self):
        self.position[1] += self.speed

    def update(self):
        self.move()

# Settings
WIDTH = 1200
HEIGHT = 800
FPS = 60
BGCOLOR = 'skyblue'

# Init
py.init()
screen = py.display.set_mode((WIDTH, HEIGHT), py.HWSURFACE | py.DOUBLEBUF | py.SCALED, vsync=1)
font = py.font.SysFont("Arial" , 18 , bold = True)
clock = py.time.Clock()
py.mouse.set_visible(False)
py.display.set_caption('Geo Gats!')
game_active = True

# Images
map = py.image.load('images/bg/eq_earth.png').convert_alpha()
cursor_icon = py.image.load('images/cursor.png').convert_alpha()
square_icon = py.image.load('images/square.png').convert_alpha()
logo_icon = py.image.load('images/globe.png').convert_alpha()
py.display.set_icon(logo_icon)
bullet_icon = py.image.load('images/bullet.png').convert_alpha()

#Groups
background = Background()
player = py.sprite.GroupSingle()
player.add(Player())
cursor = py.sprite.GroupSingle()
cursor.add(Cursor())
bullet = py.sprite.GroupSingle()
fps_counter = FPS_Counter()

# Global Variables
bullets = []

# Game loop
while game_active:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()

    screen.fill(BGCOLOR)
    background.update(player.sprite.x, player.sprite.y)
    player.draw(screen)
    player.update()
    cursor.draw(screen)
    cursor.update()
    fps_counter.update()                                                       #####

    py.display.update()
    py.event.pump()
    clock.tick(FPS)
