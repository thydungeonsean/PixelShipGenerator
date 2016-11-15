from random import *
import time
from ..constants import *
from frame import Frame
from palette import Palette
import os
import sys


def set_ship_count():

    pathname = os.path.dirname(sys.argv[0]) + '/screenshots/'

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
        return max(existing_pics)
    else:
        return 0


class Ship(object):

    """ The ship object is instantiated by generator.
    It holds a 2d list of the pixels of the ship and returns
    an image of the ship

    Map:
    0 - blank, not part of ship
    -1 - black, part of ship, but to show texture
    1 - colored pixel

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

    def __init__(self, (w, h), animating=False):

        self.ship_id = str(Ship.count)
        Ship.count += 1

        self.map = [[0 for y in range(h)] for x in range(w)]
        self.w = w
        self.h = h
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

        self.pixels = set()
        self.edges = set()

        self.generate_ship(animating)

        self.image, self.rect = self.set_image()
        # print self.frame.layout

    def set_frame(self):

        return Frame.rand_premade(self)
        # return Frame.preselected(self, 'talon')
        # return Frame.random(self)

    def pixel_on_map(self, (x, y)):

        if 0 <= x < self.w and 0 <= y < self.h:
            return True
        else:
            return False

    def change_pixel(self, (x, y), value):

        if self.pixel_on_map((x, y)):
            if value != 0:
                self.map[x][y] = value
                if value == 1:
                    self.pixels.add((x, y))
                elif value == -1:
                    self.edges.add((x, y))

    def set_image(self):

        image = pygame.Surface((self.w, self.h))
        image.fill(BLACK)

        pix_array = pygame.PixelArray(image)
        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] == 1:
                    pix_array[x, y] = self.color
                elif self.map[x][y] == -1:
                    pix_array[x, y] = BLACK

        scaled = pygame.transform.scale(image, (scale(self.w), scale(self.h)))
        image = scaled.convert()
        rect = image.get_rect()

        return image, rect

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

    # for debugging
    def print_map(self):

        for y in range(self.h):
            line = ''
            for x in range(self.w):
                if self.map[x][y] == 0:
                    new = '  '
                elif self.map[x][y] == 1:
                    new = ' #'
                elif self.map[x][y] == -1:
                    new = ' -'
                line += new
            print line

    def attach(self, component):

        for x, y in component.points:
            rx = x + component.x
            ry = y + component.y
            self.change_pixel((rx, ry), component.map[x][y])

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

        overlap = rel_points.intersection(self.pixels)

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

    def grow_out_placement(self, c, animating):

        # find a point along existing edge of ship
        # generate a component containing that point

        # check - move until placed or x cycles

        pass

    def move_and_check_placement(self, c, animating):

        placer = ComponentPlacer(self, c)

        if animating:
            ci, cr = c.set_image(self.color)

        # check if good position - adjust - iterate
        count = 0
        attached = False
        while not attached:

            if animating:
                self.animate(c, ci, cr)

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

    def animate(self, c, ci, cr):

        self.image, self.rect = self.set_image()
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)

        x = scale(c.x)
        y = scale(c.y)
        cr.topleft = x, y

        screen.blit(ci, cr)
        # time.sleep(0.05)
        pygame.display.update()

    def fill_gaps(self):

        gaps = set()

        for y in range(self.h):
            for x in range(self.w):
                if (x, y) not in self.pixels and (x, y) not in self.edges:
                    if self.point_is_gap((x, y)):
                        gaps.add((x, y))

        for point in gaps:
            self.change_pixel(point, 1)

    def point_is_gap(self, (x, y)):

        adj = ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
               (x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1))
        edges = 0
        for ax, ay in adj:
            if self.pixel_on_map((ax, ay)) and self.map[ax][ay] == -1:
                edges += 1

        return edges >= randint(5, 6)


class ComponentPlacer(object):

    directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))

    def __init__(self, ship, component):

        self.ship = ship
        self.component = component

        self.move_log = []
        self.move_dict = {}

        self.vector = None
        self.vector_log = []

        self.reversed_once = False

    def record(self, pos, state):

        self.move_log.append(pos)
        self.move_dict[pos] = state

    @property
    def current_position(self):
        if len(self.move_log) < 1:
            return None
        return self.move_log[-1]

    @property
    def current_state(self):
        if self.current_position is None:
            return None
        return self.move_dict[self.current_position]

    @property
    def previous_position(self):
        if len(self.move_log) > 1:
            return self.move_log[-2]
        return None

    @property
    def previous_state(self):
        if self.previous_position is None:
            return None
        return self.move_dict[self.previous_position]

    def place(self, start=randint(0, 1)):

        # if this is first placement of component, we do it randomly within the frame
        if not self.move_log:
            if start == 0:
                return self.get_start_point_in_frame()
            elif start == 1:
                return self.get_start_point_on_edge()

        current_state = self.current_state
        previous_state = self.previous_state

        # if component is not connected to ship or spine, we try to shift it to the center of
        # the map hopefully to connect
        if current_state == 'unconnected':
            if previous_state == 'unconnected' or previous_state is None:
                self.move_towards_center()
                return self.move_on_vector()
            elif not self.reversed_once:  # we went from connected to unconnected - no good, find new solution
                self.reverse_vector()
                self.reversed_once = True
                return self.move_on_vector()
            else:
                self.reversed_once = False
                self.set_random_vector()
                return self.move_on_vector()

        # if we are connected but overlapping, try and move so that we reduce amount overlapping
        # at beginning, pick a random direction
        if previous_state is None or previous_state == 'unconnected':
            self.set_random_vector()
            return self.move_on_vector()

        if previous_state <= current_state:
            # keep going same way
            return self.move_on_vector()

        if previous_state > current_state:
            self.set_new_vector()
            return self.move_on_vector()

    def set_new_vector(self):

        previous = set(self.vector_log)
        diff = tuple(set(ComponentPlacer.directions).difference(previous))
        if not diff:
            self.set_random_vector()
        else:
            choice(diff)

    def reverse_vector(self):
        new = []
        for i in self.vector:
            if i == 1:
                n = -1
            elif i == 0:
                n = 0
            elif i == -1:
                n = 1
            new.append(n)
        new_vector = tuple(new)
        self.change_vector(new_vector)

    def move_on_vector(self):
        dx, dy = self.vector
        cx, cy = self.current_position
        return dx + cx, dy + cy

    def set_random_vector(self):
        vector = choice(ComponentPlacer.directions)
        self.update_vector(vector)

    def update_vector(self, vector):
        self.vector_log = []
        self.vector = vector

    def change_vector(self, new):
        self.vector_log.append(self.vector)
        self.vector = new

    def move_towards_center(self):

        cx, cy = self.current_position
        if cx >= self.component.w / 2:
            dx = -1
        else:
            dx = 1
        if cy >= self.component.h / 2:
            dy = -1
        else:
            dy = 1
        self.update_vector((dx, dy))

    def get_start_point_in_frame(self):

        c = self.component

        ix, iy = self.ship.frame.point_in_frame()
        xvar = c.w / 2
        yvar = c.h / 2
        ix += randint(-xvar, xvar)
        iy += randint(-yvar, yvar)

        return ix, iy

    def get_start_point_on_edge(self):

        if not self.ship.edges:
            return self.get_start_point_in_frame()

        c = self.component

        ix, iy = choice(tuple(self.ship.edges))
        xvar = c.w / 2
        yvar = c.h / 2
        ix += randint(-xvar, xvar)
        iy += randint(-yvar, yvar)

        return ix, iy
