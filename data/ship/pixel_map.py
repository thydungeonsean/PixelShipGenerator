from ..constants import *


class PixelMap(object):

    def __init__(self, (w, h)):

        self.w = w
        self.h = h

        self.map = [[0 for my in range(h)] for mx in range(w)]

        self.points = set()
        self.edges = set()

    def set_image(self, color, fill_color=BLACK, colorkey=False):

        image = pygame.Surface((self.w, self.h))
        image.fill(fill_color)

        pix_array = pygame.PixelArray(image)
        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] == 1:
                    pix_array[x, y] = color
                elif self.map[x][y] == -1:
                    pix_array[x, y] = BLACK

        scaled = pygame.transform.scale(image, (scale(self.w), scale(self.h)))
        image = scaled.convert()

        if colorkey:
            image.set_colorkey(WHITE)

        rect = image.get_rect()

        return image, rect

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

    def is_on_map(self, (x, y)):

        if 0 <= x < self.w and 0 <= y < self.h:
            return True
        else:
            return False

    def get_adj(self, (x, y)):

        raw_adj = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        adj = set()
        for p in raw_adj:
            if self.is_on_map(p):
                adj.add(p)

        return adj

    # transforming methods
    def transform(self, method='clockwise'):
        new_w = self.h
        new_h = self.w
        new_map = [[0 for y in range(new_h)] for x in range(new_w)]
        new_points = set()
        new_edges = set()

        # transpose coordinates
        function_map = {
            'clockwise': self.clockwise_offset,
            'counter_clockwise': self.counter_clockwise_offset
            }
        self.rotate(function_map[method], new_map, new_edges, new_points)

        # replace map attributes
        self.map = new_map
        self.w = new_w
        self.h = new_h
        self.points = new_points
        self.edges = new_edges

    def rotate(self, rotate_func, new_map, new_edges, new_points):

        for i in range(self.h):

            row_coords = self.get_row(i)
            col_coords = self.get_col(rotate_func(i))

            for indx in range(self.w):
                rx, ry = row_coords[indx]
                cx, cy = col_coords[indx]
                value = self.map[rx][ry]
                new_map[cx][cy] = value
                if value == -1:
                    new_edges.add(value)
                elif value == 1:
                    new_points.add(value)

    def clockwise_offset(self, i):
        return self.h - 1 - i

    def counter_clockwise_offset(self, i):
        return i

    def get_row(self, y):
        row = []
        for x in range(self.w):
            row.append((x, y))
        return row

    def get_col(self, x):
        col = []
        for y in range(self.w):
            col.append((x, y))
        return col
