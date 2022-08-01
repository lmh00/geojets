import pygame as py
from sys import exit
import math

# Classes
class Background():
    def update(self, camX, camY):
        screen.blit(map, BACKGROUND_POSITION, (-SCREEN_CENTER_X + camX, -SCREEN_CENTER_Y + camY, SCREEN_WIDTH, SCREEN_HEIGHT))

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
        self.rect = self.image.get_rect(center = (SCREEN_CENTER_X, SCREEN_CENTER_Y))
        self.x = 5000
        self.y = 5000
        self.angle = 0
        self.speed = PLAYER_SPEED
        self.fire = BULLET_FIRERATE

    def move(self):
        pressed = py.key.get_pressed()
        if pressed[py.K_w]:
            self.speed += PLAYER_SPEED_RATE
        if pressed[py.K_s]:
            self.speed -= PLAYER_SPEED_RATE
        if pressed[py.K_a]:
            self.angle += PLAYER_TURN_RATE
        if pressed[py.K_d]:
            self.angle -= PLAYER_TURN_RATE
        if self.speed > PLAYER_MAX_SPEED:
            self.speed = PLAYER_MAX_SPEED
        if self.speed < PLAYER_MIN_SPEED:
            self.speed = PLAYER_MIN_SPEED
        self.vx = self.speed * math.sin(math.radians(self.angle))
        self.vy = self.speed * math.cos(math.radians(self.angle))
        self.x -= self.vx
        self.y -= self.vy
        self.image = py.transform.rotate(self.img, self.angle)
        self.rect = self.image.get_rect(center = (SCREEN_CENTER_X, SCREEN_CENTER_Y))

    def shoot(self):
        if py.mouse.get_pressed() == (1, 0, 0):
            self.fire += 1
            if self.fire > BULLET_FIRERATE:
                bullet.add(Bullet(self.angle))
                self.fire = 0
        else:
            self.fire = BULLET_FIRERATE

    def update(self):
        self.move()
        self.shoot()

class Bullet(py.sprite.Sprite):
    def __init__(self, angle):
        super().__init__()
        self.x = SCREEN_CENTER_X
        self.y = SCREEN_CENTER_Y
        self.rect = py.Rect(self.x, self.y, BULLET_SIZE, BULLET_SIZE)
        self.angle = math.radians(angle)
        self.dx = math.cos(self.angle) * BULLET_SPEED
        self.dy = math.sin(self.angle) * BULLET_SPEED
        self.begin = py.time.get_ticks()

    def end(self):
        if py.time.get_ticks() > (self.begin + BULLET_LIFE):
            self.kill()

    def move(self):
        self.y -= math.cos(self.angle) * BULLET_SPEED
        self.x -= math.sin(self.angle) * BULLET_SPEED
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def collide(self):
        if py.sprite.groupcollide(enemy, bullet, True, True):
            score.score += 1

    def draw(self):
        py.draw.rect(screen, BULLET_COLOR, self.rect)

    def update(self):
        self.end()
        self.move()
        self.collide()
        self.draw()

class Score():
    def __init__(self):
        super().__init__()
        self.score = 0

    def update(self):
        show_score = font.render(str(self.score) , 1, py.Color("BLACK"))
        screen.blit(show_score, (0, 50))

class Enemy(py.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.img = jet_icon
        self.image = self.img
        self.rect = self.image.get_rect(center = ((self.x + SCREEN_CENTER_X), (self.y + SCREEN_CENTER_Y)))
        self.speed = PLAYER_SPEED
        self.fire = BULLET_FIRERATE

    def update(self, camX, camY):
        self.rect = self.image.get_rect(center = ((self.x + SCREEN_CENTER_X) - camX, (self.y + SCREEN_CENTER_Y) - camY))

# Settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_CENTER_X = SCREEN_WIDTH / 2
SCREEN_CENTER_Y = SCREEN_HEIGHT / 2
FPS = 60
BACKGROUND_COLOR = 'red'
BACKGROUND_POSITION = (0, 0)
PLAYER_SPEED = 5
PLAYER_SPEED_RATE = 0.1
PLAYER_TURN_RATE = 2
PLAYER_MAX_SPEED = 10
PLAYER_MIN_SPEED = 1
BULLET_FIRERATE = 15
BULLET_COLOR = 'black'
BULLET_SIZE = 4
BULLET_SPEED = 20
BULLET_LIFE = 1000

# Init
py.init()
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), py.HWSURFACE | py.DOUBLEBUF | py.SCALED, vsync=1)
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
enemy = py.sprite.Group()
enemy.add(Enemy(200, 200))
cursor = py.sprite.GroupSingle()
cursor.add(Cursor())
bullet = py.sprite.Group()
score = Score()
fps_counter = FPS_Counter()

#Global Variables
ex = 5100
ey = 5100

# Game loop
while game_active:
    camX, camY = player.sprite.x, player.sprite.y
    x, y = py.mouse.get_pos() # needed for b in bullets

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()

    screen.fill(BACKGROUND_COLOR)
    background.update(camX, camY)
    player.update()
    player.draw(screen)
    enemy.update(camX, camY)
    enemy.draw(screen)
    cursor.update()
    cursor.draw(screen)
    bullet.update()
    score.update()
    fps_counter.update()

    if py.time.get_ticks() // 1000 > len(enemy):
        enemy.add(Enemy(ex, ey))
        ex += 100
        ey += 100

    py.display.update()
    py.event.pump()
    clock.tick(FPS)
