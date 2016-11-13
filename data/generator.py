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
    def generate_ship(w=descale(SHIPW), h=descale(SHIPH), animating=False):
        s = Ship((w, h), animating)
        return s

    def __init__(self, main):

        self.main = main

        self.grid_ref = self.set_grid()
        self.ship_grid = {}

        self.show_frame = False
        self.show_spine = False

        self.fill_grid()

    def fill_grid(self):

        for i in Generator.grid_points:
            point = self.grid_ref[i]
            ship = self.generate_ship(animating=False)

            self.ship_grid[point] = ship
            self.draw(pygame.display.get_surface())
            pygame.display.update()

    def draw(self, surface):

        for (x, y), ship in self.ship_grid.items():
            point = x*SHIPW, y*SHIPH
            i, r = ship.get_image(self.show_frame, self.show_spine)
            r.topleft = point
            surface.blit(i, r)

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.main.end_main()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.main.end_main()

                elif event.key == K_SPACE:
                    self.fill_grid()
