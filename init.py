import pygame as py
from settings import *

py.init()
screen = py.display.set_mode((HEIGHT, WIDTH))
font = py.font.SysFont("Arial" , 18 , bold = True)
clock = py.time.Clock()
py.mouse.set_visible(False)
py.display.set_icon(logo_icon)
py.display.set_caption('Geo Jets!')
game_active = True
