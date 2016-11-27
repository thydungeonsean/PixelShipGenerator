import pygame
from pygame.locals import *
from data.constants import *
import data.ship.components.basic_hull as bh
import data.ship.components.compound_components as cc
import data.ship.components.curves as cv
import time
import data.ship.ship as ship
from random import *


screen = pygame.display.get_surface()

uss = ship.Ship((50, 50))
uss.draw(screen)

pygame.display.update()

end = False
while not end:
    if pygame.event.wait().type == KEYDOWN:
        end = True

uss.center_ship()
uss.draw(screen)
pygame.display.update()

end = False
while not end:
    if pygame.event.wait().type == KEYDOWN:
        end = True

pygame.quit()


