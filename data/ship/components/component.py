import pygame
from ...constants import *


class Component(object):
    
    """ This is the base class for a ship
    component. It should not be directly created.
    Create() must be overwritten by subclass. This
    sets the initial value of the map
    """

    def __init__(self, (w, h), coord=(0, 0), autocreate=True, autooutline=True):

        self.w = w
        self.h = h
        
        self.x, self.y = coord

        self.map = [[0 for my in range(h)] for mx in range(w)]
        
        self.points = set()
        self.edges = set()

        if autocreate:
            self.create()
            if autooutline:
                self.outline()

    def set_image(self, c):

        image = pygame.Surface((self.w, self.h))
        image.fill(WHITE)

        pix_array = pygame.PixelArray(image)
        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] == 1:
                    pix_array[x, y] = c
                elif self.map[x][y] == -1:
                    pix_array[x, y] = BLACK

        scaled = pygame.transform.scale(image, (scale(self.w), scale(self.h)))
        image = scaled.convert()
        image.set_colorkey(WHITE)
        rect = image.get_rect()

        return image, rect

    def create(self):
        pass

    def add_pixel(self, (x, y), value=1):

        self.map[x][y] = value
        self.points.add((x, y))

    def add_edge(self, (x, y)):

        self.map[x][y] = -1
        self.edges.add((x, y))

    def trim_edge(self, (x, y)):

        self.map[x][y] = 0
        self.edges.remove((x, y))
        self.points.remove((x, y))

    def outline(self, trim=False):
    
        outline = set()
        for x, y in self.points:

            if y == 0 or y == self.h-1 or x == 0 or x == self.w-1:
                outline.add((x, y))
                continue

            adj = self.get_adj((x, y))
            for ax, ay in adj:
                if self.map[ax][ay] == 0:
                    outline.add((x, y))
                    break
                    
        for px, py in outline:
            self.add_edge((px, py))

        if trim:
            self.trim_outline(outline)

    def trim_outline(self, outline):

        trim = set()

        for x, y in outline:
            adj = self.get_adj((x, y))
            next_to_pixel = False
            for ax, ay in adj:
                if self.map[ax][ay] == 1:
                    next_to_pixel = True
                    break
            if not next_to_pixel:
                trim.add((x, y))

        for tx, ty in trim:
            self.trim_edge((tx, ty))

    def get_adj(self, (x, y)):

        raw_adj = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        adj = set()
        for p in raw_adj:
            if self.is_on_map(p):
                adj.add(p)

        return adj
       
    ##################################################################
    # realized this floodfill to outline was needlessly complicated
    # and would also fail to outline internal details
    def flood_outline(self):

        # flood fill from edge of map to set a border or black
        # around component

        edge = self.get_edge_set()
        seen = set()

        while edge:
            next = set()
            for x, y in edge:
                seen.add((x, y))
                if self.map[x][y] == 1:
                    self.map[x][y] = -1
                elif self.map[x][y] == 0:
                    next.add((x, y))
            edge = self.get_next_edge(next, seen)

    def get_next_edge(self, next, seen):

        edge = set()

        for point in next:
            adj = self.get_adj(point)
            for p in adj:
                if p not in seen:
                    edge.add(p)
        return edge
        
    def get_edge_set(self):

        edge = set()

        for y in range(self.h):
            for x in range(self.w):
                if y == 0 or y == self.h - 1:
                    edge.add((x, y))
                elif x == 0 or x == self.w - 1:
                    edge.add((x, y))

        return edge
    ####################################################################

    def is_on_map(self, (x, y)):

        if 0 <= x < self.w and 0 <= y < self.h:
            return True
        else:
            return False

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

    def get_relative_points(self, edge=False):

        if edge:
            pointset = self.edges
        else:
            pointset = self.points

        rel = set()
        for x, y in pointset:
            nx = x + self.x
            ny = y + self.y
            rel.add((nx, ny))

        return rel

    # adds a component object's map to current map
    def add(self, component):

        sx = component.x
        sy = component.y
        w = component.w
        h = component.h

        for y in range(h):
            for x in range(w):
                mx = sx + x
                my = sy + y
                c_value = component.map[x][y]
                if c_value != 0:
                    self.add_pixel((mx, my), value=c_value)

    def move(self, (x, y)):

        self.x = x
        self.y = y

    # transforming methods
    def transform(self, direction):

        new_w = self.h
        new_h = self.w
        new_map = [[0 for y in range(new_h)] for x in range(new_w)]
        new_points = set()
        new_edges = set()

        # transpose coordinates

        self.map = new_map
        self.w = new_w
        self.h = new_h
        self.points = new_points
        self.edges = new_edges
