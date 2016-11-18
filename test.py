import pygame
from pygame.locals import *
from data.constants import *
import data.ship.components.basic_hull as bh
import time


s = pygame.display.get_surface()

c = bh.AngleTopRight(80)
i, r = c.set_image(RED, fill_color=WHITE)

s.blit(i, r)

pygame.display.update()
time.sleep(.5)
s.fill(BLACK)

c.transform(method='counter_clockwise')
i, r = c.set_image(RED, fill_color=WHITE)
s.blit(i, r)

pygame.display.update()
time.sleep(2)