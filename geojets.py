import pygame as py
from sys import exit
import math
import random

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

class FPS_Counter():
    def update(self):
        fps = str(int(clock.get_fps()))
        fps_t = font.render(fps , 1, py.Color("RED"))
        screen.blit(fps_t,(0,0))

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = jet_icon
        self.image = self.img
        self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self.x = 5000
        self.y = 5000
        self.speed = 5
        self.load = 5

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
        mx, my = py.mouse.get_pos()
        angleRad = math.atan2(self.rect.centery - my, mx - self.rect.centerx)
        angleDeg = math.degrees(angleRad) - 90
        self.image = py.transform.rotate(self.img, angleDeg)
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))

    def shoot(self):
        if py.mouse.get_pressed() == (1, 0, 0):
            self.load += 1
            if self.load > 5:
                b = Bullet(x, y)
                bullets.append(b)
                self.load = 0

    def update(self):
        self.turn()
        self.rotate()
        self.shoot()

class Bullet():
    def __init__(self, mx, my):
        super().__init__()
        self.x = (WIDTH / 2)
        self.y = (HEIGHT / 2)
        self.mx = mx
        self.my = my
        self.color = 'black'
        self.width = 3
        self.height = 3
        self.rect = py.Rect(self.x, self.y, self.width, self.height)
        self.speed = random.randrange(30, 50)
        self.angle = math.atan2(self.my - self.y, self.mx - self.x)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.begin = py.time.get_ticks()

    def end(self, b):
        if py.time.get_ticks() > (self.begin + 1000):
            bullets.pop(b)

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self):
        py.draw.rect(screen, self.color, self.rect)

    def update(self, b):
        self.end(bullets.index(b))
        self.move()
        self.draw()

# Settings
WIDTH = 1200
HEIGHT = 800
FPS = 60
BGCOLOR = 'red'

# Init
py.init()
screen = py.display.set_mode((WIDTH, HEIGHT), py.HWSURFACE | py.DOUBLEBUF | py.SCALED, vsync=1)
font = py.font.SysFont("Arial" , 18 , bold = True)
clock = py.time.Clock()
py.mouse.set_visible(False)
py.display.set_caption('Geo Jets!')
game_active = True

# Images -- you can put this all in one image when finished
map = py.image.load('images/bg/eq_earth.png').convert_alpha()
cursor_icon = py.image.load('images/cursor.png').convert_alpha()
jet_icon = py.image.load('images/jet.png').convert_alpha()
logo_icon = py.image.load('images/globe.png').convert_alpha()
py.display.set_icon(logo_icon) # has to come after logo_icon

#Global Variables
bullets = []

#Groups
background = Background()
player = py.sprite.GroupSingle()
player.add(Player())
cursor = py.sprite.GroupSingle()
cursor.add(Cursor())
fps_counter = FPS_Counter()

FIRERATE = 1001

# Game loop
while game_active:
    x, y = py.mouse.get_pos()

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
    fps_counter.update()

    for b in bullets:
        b.update(b)

    py.display.update()
    py.event.pump()
    clock.tick(FPS)
