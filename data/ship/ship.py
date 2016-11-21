from random import *
import time
from pixel_map import PixelMap
from ..constants import *
from frame import Frame
from palette import Palette
import component_placer as cp
import os
import sys


def set_ship_count():

    pathname = os.pardir + '/exports/'

    existing_pics = []

    for file in os.listdir(pathname):
        fname = pathname + file
        if os.path.isfile(fname) and file.endswith('.png') and file.startswith('ship'):
            num = file.rstrip('.png')
            num = num.lstrip('ship')
            try:
                num = int(num)
                existing_pics.append(num)
            except ValueError:
                pass
    if len(existing_pics) > 0:
        return max(existing_pics)+1
    else:
        return 0


class Ship(PixelMap):

    """ The ship object is instantiated by generator.
    It holds a 2d list of the pixels of the ship and returns
    an image of the ship

    Map:ure
    1 - colored pixel
    0 - blank, not part of ship
    -1 - black, part of ship, but to show text

    """

    # TODO - find a non messy way to move this function into class
    count = set_ship_count()

    @staticmethod
    def set_random_color():

        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        return r, g, b
        #return RED

    def __init__(self, (w, h), animating=False, grid_coord=(0, 0)):

        self.ship_id = str(Ship.count)
        Ship.count += 1
        self.grid_coord = grid_coord

        PixelMap.__init__(self, (w, h))

        self.color = self.set_random_color()
        self.frame = self.set_frame()
        self.spine = self.frame.spine
        self.palette = Palette()

        # conformity is percentage of tiles per component that should be in frame
        self.conformity = .55
        # size is % of frame that must be filled to complete component stage
        self.size = .75
        self.frame_size = self.frame.size
        self.points_in_frame = 0

        self.generate_ship(animating)

        self.image, self.rect = self.set_image(self.color)
        # print self.frame.layout

    # pixel map funtions
    def transform(self, method):
        if method not in ('clockwise', 'counter_clockwise', 'ver_flip', 'hor_flip'):
            print '***************** invalid transform keyword ********************'
            return
        self._transform(method)
        self.update_id()

    def update_id(self):
        self.ship_id = str(Ship.count)
        Ship.count += 1

    def set_frame(self):

        return Frame.rand_premade(self)
        # return Frame.preselected(self, 'talon')
        # return Frame.random(self)

    # def change_pixel(self, (x, y), value):
    #
    #     if self.is_on_map((x, y)):
    #         if value != 0:
    #             self.map[x][y] = value
    #             if value == 1:
    #                 self.points.add((x, y))
    #             elif value == -1:
    #                 self.edges.add((x, y))

    def get_image(self, frame=False, spine=False):

        if frame or spine:
            i = self.image.copy()
            if frame:
                self.show_frame(i)
            if spine:
                self.show_spine(i)
        else:
            i = self.image

        return i, self.rect

    def update_image(self, fill_color=BLACK, colorkey=False):
        self.image, self.rect = self.set_image(self.color, fill_color, colorkey)

    def show_frame(self, image):

        for zone in self.frame.zones:

            x = scale(zone.x1)
            y = scale(zone.y1)
            w = scale(zone.w)
            h = scale(zone.h)

            r = pygame.Rect((x, y), (w, h))
            pygame.draw.rect(image, YELLOW, r, 1)

        # print self.frame.layout

    def show_spine(self, image):

        for x, y in self.spine.points:
            ax = scale(x)
            ay = scale(y)
            pygame.draw.line(image, RED, (ax, ay), (ax, ay))

    def attach(self, component):

        points = component.points.copy()
        points.update(component.edges)

        for x, y in points:
            rx = x + component.x
            ry = y + component.y
            self.add_point((rx, ry), component.map[x][y])

            if self.frame.is_in_frame((rx, ry)):
                self.points_in_frame += 1

    def is_connected_to_ship(self, c):

        rel_points = c.get_relative_points()

        # check if connected to spine
        on_spine = rel_points.intersection(self.spine.points)
        if on_spine:
            return True

        rel_edges = c.get_relative_points(edge=True)
        on_edges = rel_edges.intersection(c.edges)
        if on_edges:
            return True

        return False

    def is_overlapping(self, c):

        rel_points = c.get_relative_points()

        overlap = rel_points.intersection(self.points)

        if overlap:
            return True, len(overlap)
        else:
            return False, 0

    def is_in_frame(self, c):

        rel_points = c.get_relative_points()
        max = float(len(rel_points))
        in_frame = 0

        for point in rel_points:
            if self.frame.is_in_frame(point):
                in_frame += 1

        ratio = in_frame / max
        if ratio >= self.conformity:
            return True
        return False

    def add_component(self, component, animating):

        # select a start position on ship map
        # check if connected
        # check if not overlapping
        # if those pass, check if in frame
        # needs methods to move position intelligently to meet conditions

        c = component

        self.move_and_check_placement(c, animating)

    # def grow_out_placement(self, c, animating):

        # find a point along existing edge of ship
        # generate a component containing that point

        # check - move until placed or x cycles

        # pass

    def move_and_check_placement(self, c, animating):

        placer = cp.ComponentPlacer(self, c)

        if animating:
            c.update_image(self.color, fill_color=WHITE, colorkey=WHITE)

        # check if good position - adjust - iterate
        count = 0
        attached = False
        while not attached:

            if animating:
                self.animate(c)

            count += 1
            if count > 20:
                return

            # place component
            position = placer.place()
            c.move(position)

            # check if component on spine, or attached to existing components
            connected = self.is_connected_to_ship(c)
            if not connected:
                placer.record(position, 'unconnected')
                continue

            # check if component overlaps existing components
            overlapping, over = self.is_overlapping(c)
            if overlapping:
                placer.record(position, over)
                continue

            in_frame = self.is_in_frame(c)
            if not in_frame:
                placer.record(position, 0)
                continue

            attached = connected

        self.attach(c)
        if animating:
            self.animate(c)
            if c.name == 'angle':
                print c.edges
            while True:
                if pygame.event.wait().type == KEYDOWN:
                    return

    def generate_ship(self, animating=False):

        count = 0
        while self.frame_not_full():

            count += 1
            c = self.palette.get_component()

            self.add_component(c, animating)
            if count > 100:
                break

        self.fill_gaps()

    def frame_not_full(self):
        ratio = self.points_in_frame / float(self.frame_size)

        if ratio < self.size:
            return True
        else:
            return False

    def get_grid_coord(self):

        x, y = self.grid_coord
        x *= SHIPW
        y *= SHIPH
        y += BUTTONMARGIN
        return x, y

    def animate(self, component):

        self.update_image(self.color)
        sx, sy = self.get_grid_coord()
        self.rect.topleft = (sx, sy)
        screen = pygame.display.get_surface()
        self.draw(screen)

        x = scale(component.x) + sx
        y = scale(component.y) + sy
        component.rect.topleft = x, y

        component.draw(screen)
        # time.sleep(0.05)
        pygame.display.update()

    def fill_gaps(self):

        gaps = set()

        for y in range(self.h):
            for x in range(self.w):
                if (x, y) not in self.points and (x, y) not in self.edges:
                    if self.point_is_gap((x, y)):
                        gaps.add((x, y))

        for point in gaps:
            self.change_point(point, 1)

    def point_is_gap(self, (x, y)):

        adj = ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
               (x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1))
        edges = 0
        for ax, ay in adj:
            if self.is_on_map((ax, ay)) and self.map[ax][ay] == -1:
                edges += 1

        return edges >= randint(5, 6)
