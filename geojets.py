import pygame as py
from sys import exit
import math

# Classes
class Background():
    def update(self, px, py):
        screen.blit(map, BG_POS, (-SCX + px, -SCY + py, SW, SH))

class Cursor(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cursor_icon
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = py.mouse.get_pos()

class FPS_Counter():
    def update(self):
        fps = str(int(clock.get_fps()))
        fps_t = font.render(fps , 1, py.Color("RED"))
        screen.blit(fps_t, (0, 0))

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = jet_icon
        self.image = self.img
        self.rect = self.image.get_rect(center = (SCX, SCY))
        self.x = 100
        self.y = 100
        self.speed = PLYR_SPEED
        self.load = LOAD_SPEED

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
        angleDeg = math.degrees(angleRad) - 90 # sprite is angled wrong w/o -90
        self.image = py.transform.rotate(self.img, angleDeg)
        self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))

    def shoot(self):
        if py.mouse.get_pressed() == (1, 0, 0):
            self.load += 1
            if self.load > LOAD_SPEED:
                b = Bullet(x, y)
                bullets.append(b)
                self.load = 0
        else:
            self.load = LOAD_SPEED

    def update(self):
        self.turn()
        self.rotate()
        self.shoot()

class Bullet():
    def __init__(self, mx, my):
        super().__init__()
        self.x = SCX
        self.y = SCY
        self.mx = mx
        self.my = my
        self.rect = py.Rect(self.x, self.y, BULLET_SIZE, BULLET_SIZE)
        self.angle = math.atan2(self.my - self.y, self.mx - self.x)
        self.dx = math.cos(self.angle) * BULLET_SPEED
        self.dy = math.sin(self.angle) * BULLET_SPEED
        self.begin = py.time.get_ticks()

    def end(self, b):
        if py.time.get_ticks() > (self.begin + BULLET_LIFE):
            bullets.pop(b)

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self):
        py.draw.rect(screen, BULLET_COLOR, self.rect)

    def update(self, b):
        self.end(bullets.index(b))
        self.move()
        self.draw()

class Enemy(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 200
        self.y = 200
        self.img = jet_icon
        self.image = self.img
        self.speed = PLYR_SPEED
        self.load = LOAD_SPEED

    def update(self, px, py):
        self.rect = self.image.get_rect(center = ((self.x + SCX) - px, (self.y + SCY) - py ))


# Settings
SW = 1200
SH = 800
SCX = SW / 2
SCY = SH / 2
FPS = 60
BG_COLOR = 'red'
BG_POS = (0, 0)
PLYR_SPEED = 5
LOAD_SPEED = 15
BULLET_COLOR = 'black'
BULLET_SIZE = 4
BULLET_SPEED = 20
BULLET_LIFE = 1000

# Init
py.init()
screen = py.display.set_mode((SW, SH), py.HWSURFACE | py.DOUBLEBUF | py.SCALED, vsync=1)
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

#Groups
background = Background()
player = py.sprite.GroupSingle()
player.add(Player())
enemy = py.sprite.GroupSingle()
enemy.add(Enemy())
cursor = py.sprite.GroupSingle()
cursor.add(Cursor())
fps_counter = FPS_Counter()

#Global Variables
bullets = []

# Game loop
while game_active:
    x, y = py.mouse.get_pos() # needed for b in bullets

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()

    screen.fill(BG_COLOR)
    background.update(player.sprite.x, player.sprite.y)
    player.update()
    player.draw(screen)
    enemy.update(player.sprite.x, player.sprite.y)
    enemy.draw(screen)
    cursor.update()
    cursor.draw(screen)
    fps_counter.update()

    for b in bullets:
        b.update(b)

    py.display.update()
    py.event.pump()
    clock.tick(FPS)
