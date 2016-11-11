from constants import *
from ship.ship import Ship
from ship.components import basic_hull
from random import *


class Generator(object):

    gridw = 8
    gridh = 6
    grid_points = range(gridw * gridh)

    @classmethod
    def set_grid(cls):
        grid = {}

        gridw = cls.gridw

        for key in cls.grid_points:
            x = key % gridw
            y = key / gridw
            grid[key] = (x, y)

        return grid

    @staticmethod
    def generate_ship(w=50, h=50):
        s = Ship((w, h))
        return s

    def __init__(self):

        self.grid_ref = self.set_grid()
        self.ship_grid = {}

        self.fill_grid()

    def fill_grid(self):

        for i in Generator.grid_points:
            point = self.grid_ref[i]
            ship = self.generate_ship()

            self.ship_grid[point] = ship

    def draw(self, surface):

        for (x, y), ship in self.ship_grid.items():
            point = x*SHIPW, y*SHIPH
            i, r = ship.get_image()
            r.topleft = point
            surface.blit(i, r)

