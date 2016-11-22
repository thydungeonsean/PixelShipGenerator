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

        self.image, self.rect = self.set_image(self.color, fill_color=WHITE)
        # print self.frame.layout

    # pixel map funtions
    def transform(self, method):
        if method not in ('clockwise', 'counter_clockwise', 'ver_flip', 'hor_flip'):
            print '***************** invalid transform keyword ********************'
            return
        self._transform(method)
        self.update_id()

    # ship attributes
    def update_id(self):
        self.ship_id = str(Ship.count)
        Ship.count += 1

    def set_frame(self):

        return Frame.rand_premade(self)
        # return Frame.preselected(self, 'talon')
        # return Frame.random(self)

    # image methods
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

    def update_image(self, color=None, fill_color=BLACK, colorkey=False):
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

    # msin ship generating algorithm
    def generate_ship(self, animating=False):

        count = 0
        while self.frame_not_full():

            count += 1
            c = self.palette.get_component()

            self.add_component(c, animating)
            if count > 100:
                break

        self.fill_gaps()
        self.complete_outline()
        self.clear_edge()

        self.check_connected()

    # component adding methods
    def attach(self, component):

        points = component.points.copy()
        points.update(component.edges)

        for x, y in points:
            rx = x + component.x
            ry = y + component.y
            self.add_point((rx, ry), component.map[x][y])

            if self.frame.is_in_frame((rx, ry)):
                self.points_in_frame += 1

    def add_component(self, component, animating):


        # select a start position on ship map
        # check if connected
        # check if not overlapping
        # if those pass, check if in frame
        # needs methods to move position intelligently to meet conditions

        c = component

        self.move_and_check_placement(c, animating)

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
            connected = c.is_connected_to_ship(self)
            if not connected:
                placer.record(position, 'unconnected')
                continue

            # check if component overlaps existing components
            overlapping, over = c.is_overlapping(self)
            if overlapping:
                placer.record(position, over)
                continue

            in_frame = c.is_in_frame(self)
            if not in_frame:
                placer.record(position, 0)
                continue

            attached = connected

        self.attach(c)
        if animating:
            self.animate(c)

            while True:
                if pygame.event.wait().type == KEYDOWN:
                    return

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

    # for debugging
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

    # post generation modification
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

    def complete_outline(self):

        outline = set()

        for y in range(self.h):
            for x in range(self.w):
                tile = self.map[x][y]
                if tile >= 1 or tile == -1:
                    continue
                adj = self.get_adj((x, y))
                for ax, ay in adj:
                    if self.map[ax][ay] >= 1:
                        outline.add((x, y))
                        break

        for point in outline:
            self.add_edge(point)

    def clear_edge(self):

        for y in range(self.h):
            for x in range(self.w):
                if y == 0 or y == self.h-1 or x == 0 or x == self.w-1:
                    if self.map[x][y] != 0:
                        self.trim_point((x, y))

    def check_connected(self):

        connection_map = PixelMap((self.w, self.h))

        ship_chunks = self.get_chunks()
        for k, v in ship_chunks.items():
            connection_map.add_point(k, v)

        connection_map.print_map()

    def get_chunks(self):

        chunk_dict = {}

        chunk_id = 0

        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] == 0:
                    continue
                try:
                    chunk_dict[(x, y)]
                except KeyError:  # only try flood filling if it's not part of a chunk already
                    chunk_id += 1
                    self.flood_chunk((x, y), chunk_dict, chunk_id)

        print chunk_id

        return chunk_dict

    def flood_chunk(self, (x, y), dict, tag):

        dict[(x, y)] = tag

        queue = [(x, y)]

        complete = False

        while not complete:

            queue = self.flood(queue, dict, tag)

            if not queue:
                complete = True

    def flood(self, queue, dict, tag):

        next_queue = []

        for point in queue:

            neighbours = self.get_adj(point)

            for p in neighbours:
                x, y = p
                if self.map[x][y] == 0:
                    continue
                try:
                    dict[p]
                except KeyError:
                    dict[p] = tag
                    next_queue.append(p)

        return next_queue
