import pygame
from ...constants import *
from ..pixel_map import PixelMap


class Component(PixelMap):
    
    """ This is the base class for a ship
    component. It should not be directly created.
    Create() must be overwritten by subclass. This
    sets the initial value of the map
    """

    def __init__(self, (w, h), coord=(0, 0), autocreate=True, autooutline=True):

        self.x, self.y = coord

        PixelMap.__init__(self, (w, h))

        self.name = 'generic'

        if autocreate:
            self.create()
            if autooutline:
                self.outline()

    def create(self):
        pass

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

    # to be wrapped by outline in certain component types
    def alt_outline(self, trim=False):

        outline = set()

        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] >= 1:
                    continue
                adj = self.get_adj((x, y))
                for ax, ay in adj:
                    if self.map[ax][ay] >= 1:
                        outline.add((x, y))
                        break

        for point in outline:
            self.add_edge(point)

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
