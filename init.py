import pygame as py
from settings import *

py.init()
screen = py.display.set_mode((HEIGHT, WIDTH))
py.mouse.set_visible(False)
clock = py.time.Clock()
game_active = True
font = py.font.SysFont("Arial" , 18 , bold = True)

# Background images
bg1 = py.image.load('images/bg/1.png').convert_alpha()
bg2 = py.image.load('images/bg/2.png').convert_alpha()
bg3 = py.image.load('images/bg/3.png').convert_alpha()
bg4 = py.image.load('images/bg/4.png').convert_alpha()
bg5 = py.image.load('images/bg/5.png').convert_alpha()
bg6 = py.image.load('images/bg/6.png').convert_alpha()
bg7 = py.image.load('images/bg/7.png').convert_alpha()
bg8 = py.image.load('images/bg/8.png').convert_alpha()
bg9 = py.image.load('images/bg/9.png').convert_alpha()
bg10 = py.image.load('images/bg/10.png').convert_alpha()
bg11 = py.image.load('images/bg/11.png').convert_alpha()
bg12 = py.image.load('images/bg/12.png').convert_alpha()
bg13 = py.image.load('images/bg/13.png').convert_alpha()
bg14 = py.image.load('images/bg/14.png').convert_alpha()
bg15 = py.image.load('images/bg/15.png').convert_alpha()
bg16 = py.image.load('images/bg/16.png').convert_alpha()
bg17 = py.image.load('images/bg/17.png').convert_alpha()
bg18 = py.image.load('images/bg/18.png').convert_alpha()
bg19 = py.image.load('images/bg/19.png').convert_alpha()
bg20 = py.image.load('images/bg/20.png').convert_alpha()
bg21 = py.image.load('images/bg/21.png').convert_alpha()
bg22 = py.image.load('images/bg/22.png').convert_alpha()
bg23 = py.image.load('images/bg/23.png').convert_alpha()
bg24 = py.image.load('images/bg/24.png').convert_alpha()
bg25 = py.image.load('images/bg/25.png').convert_alpha()

# Other images
cursor_icon = py.image.load('images/cursor.png').convert_alpha()
jet_icon = py.image.load('images/jet.png').convert_alpha()
logo_icon = py.image.load('images/globe.png').convert_alpha()

py.display.set_icon(logo_icon)
py.display.set_caption('Geo Jets!')
