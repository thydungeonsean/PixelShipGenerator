from component import Component
from random import *


class Angle(Component):

    @classmethod
    def generate_topright_45(cls):
        w = randint(5, 7)
        return cls((w, w))

    @classmethod
    def generate_botright_45(cls):
        w = randint(5, 7)
        tr = cls((w, w))
        tr.transform('clockwise')
        return tr

    @classmethod
    def generate_botleft_45(cls):
        w = randint(5, 7)
        br = cls((w, w))
        br.transform('clockwise')
        br.transform('clockwise')
        return br

    @classmethod
    def generate_topleft_45(cls):
        w = randint(5, 7)
        bl = cls((w, w))
        bl.transform('counter_clockwise')
        return bl

    @classmethod
    def generate_topright_complement_45(cls):
        w = randint(5, 7)
        style = randint(0, 1)
        ang = cls((w, w))
        if style == 0:
            pass
        elif style == 1:
            ang.transform('clockwise')
            ang.transform('clockwise')
        return ang

    @classmethod
    def generate_topleft_complement_45(cls):
        w = randint(5, 7)
        style = randint(0, 1)
        ang = cls((w, w))
        if style == 0:
            ang.transform('clockwise')
        elif style == 1:
            ang.transform('counter_clockwise')
        return ang

    @classmethod
    def generate(cls, style=0):
        style_dict = {0: cls.generate_topleft_45,
                      1: cls.generate_topright_45,
                      2: cls.generate_botright_45,
                      3: cls.generate_botleft_45,
                      4: cls.generate_topright_complement_45,
                      5: cls.generate_topleft_complement_45
                      }
        style_num = len(style_dict)
        s = style % style_num
        return style_dict[s]()

    # not a working component - base class for 45 degree
    # angle components

    def __init__(self, (w, h), coord=(0, 0), b=0, autooutline=True):

        self.m = float(h) / w
        self.b = b

        Component.__init__(self, (w, h), coord=coord, autooutline=autooutline)
        self.name = 'angle'

    def create(self):

        for y in range(self.h):
            for x in range(self.w):
                if self.on_angle(x, y):
                    self.add_pixel((x, y))

    def on_angle(self, x, y):
        if self.line(x) <= y:
            return True
        else:
            return False

    def line(self, x):
        return int(self.m*x) + self.b
