import pygame
from random import *
from ..constants import *
from frame import Frame


class Ship(object):

    """ The ship object is instantiated by generator.
    It holds a 2d list of the pixels of the ship and returns
    an image of the ship

    Map:
    0 - blank, not part of ship
    -1 - black, part of ship, but to show texture
    1 - colored pixel

    """

    @staticmethod
    def set_random_color():

        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        return r, g, b

    def __init__(self, (w, h)):

        self.map = [[0 for y in range(h)] for x in range(w)]
        self.w = w
        self.h = h
        self.color = self.set_random_color()
        self.frame = self.set_frame()
        self.spine = self.frame.spine
        self.show_frame()
        self.show_spine()

        self.image, self.rect = self.set_image()

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

    def set_image(self):

        image = pygame.Surface((self.w, self.h))
        image.fill(BLACK)

        pix_array = pygame.PixelArray(image)
        for y in range(self.h):
            for x in range(self.w):
                if self.map[x][y] == 1:
                    pix_array[x, y] = self.color

        scaled = pygame.transform.scale(image, (scale(self.w), scale(self.h)))
        image = scaled.convert()
        rect = image.get_rect()

        return image, rect

    def get_image(self):

        return self.image, self.rect


    # TODO make a real capability to display the frame.
    # This one would destroy data from the ship if called.
    def show_frame(self):

        for zone in self.frame.zones:
            x = zone.x1
            y = zone.y1
            w = zone.w
            h = zone.h
            for zy in range(y, y+h):
                for zx in range(x, x+w):
                    draw = False
                    if zy == y or zy == y+h-1:
                        draw = True
                    elif zx == x or zx == x+w-1:
                        draw = True

                    if draw:
                        self.map[zx][zy] = 1

        print self.frame.layout

    def show_spine(self):

        for x, y in self.spine.spine:
            self.map[x][y] = 1

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
