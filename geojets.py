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
        click = py.mouse.get_pressed() == (1, 0, 0)
        mouse = py.mouse.get_pos()
        if click:
            b = Bullet(self.x, self.y, mouse[0], mouse[1])
            bullets.append(b)

    def update(self):
        self.turn()
        self.rotate()
        self.shoot()

class Bullet(py.sprite.Sprite):
    def __init__(self, px, py, mx, my):
        super().__init__()
        self.img = bullet_icon
        self.image = self.img
        self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self.speed = 1
        angle = math.atan2(my - px, mx - py)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def move(self):
        self.rect.x = self.rect.x + int(self.dx)
        self.rect.y = self.rect.y + int(self.dy)

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
py.display.set_caption('Geo Jets!')
game_active = True

# Images -- you can put this all in one image
map = py.image.load('images/bg/eq_earth.png').convert_alpha()
bullet_icon = py.image.load('images/bullet.png').convert_alpha()
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
bullet = py.sprite.GroupSingle()
fps_counter = FPS_Counter()

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
    fps_counter.update()

    for b in bullets:
        b.move()

    py.display.update()
    py.event.pump()
    clock.tick(FPS)
