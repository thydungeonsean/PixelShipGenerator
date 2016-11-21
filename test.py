import pygame
from pygame.locals import *
from data.constants import *
import data.ship.components.basic_hull as bh
import data.ship.components.compound_components as cc
import data.ship.components.curves as cv
import time
import data.ship.ship as ship
from random import *


s = pygame.display.get_surface()

c = cv.LongInvCurve.generate(randint(0, 3))
c.update_image(RED, fill_color=WHITE)
c.draw(s)

pygame.display.update()

end = False
while not end:
    if pygame.event.wait().type == KEYDOWN:
        end = True

s.fill(BLACK)
