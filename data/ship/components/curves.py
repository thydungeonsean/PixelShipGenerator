from ...constants import *
from component import *
from random import *


class LongInvCurve(Component):

    @classmethod
    def generate_br_down(cls):
        h = randint(3, 5)
        return cls(h)

    @classmethod
    def generate_br_up(cls):
        h = randint(3, 5)
        crv = cls(h)
        crv.transform('ver_flip')
        return crv

    @classmethod
    def generate_bl_up(cls):
        h = randint(3, 5)
        crv = cls(h)
        crv.transform('ver_flip')
        crv.transform('hor_flip')
        return crv

    @classmethod
    def generate_bl_down(cls):
        h = randint(3, 5)
        crv = cls(h)
        crv.transform('hor_flip')
        return crv

    @classmethod
    def generate(cls, style=0):
        style_dict = {
            0: cls.generate_br_down,
            1: cls.generate_br_up,
            2: cls.generate_bl_down,
            3: cls.generate_bl_up,
        }
        style_num = len(style_dict)
        s = style % style_num
        return style_dict[s]()

    def __init__(self, h, coord=(0, 0), autooutline=True):

        true_h = h + 2
        true_w = self.set_true_width(h)
        self.base_h = h

        Component.__init__(self, (true_w, true_h), coord=coord, autooutline=autooutline)

    @staticmethod
    def set_true_width(h):
        w = 2
        while h != 0:
            w += h
            h -= 1
        return w

    def outline(self, trim=False):
        return self.alt_outline(trim)

    def create(self):

        dim = self.w - 1
        mod = self.base_h

        for y in range(self.h):
            if y < 1 or y == self.h - 1:
                continue

            for x in range(1, dim):
                self.add_point((x, y))

            dim -= mod
            mod -= 1


class LongCurve(Component):

    @classmethod
    def generate_br_down(cls):
        h = randint(3, 5)
        return cls(h)

    @classmethod
    def generate_br_up(cls):
        h = randint(3, 5)
        crv = cls(h)
        crv.transform('ver_flip')
        return crv

    @classmethod
    def generate_bl_up(cls):
        h = randint(3, 5)
        crv = cls(h)
        crv.transform('ver_flip')
        crv.transform('hor_flip')
        return crv

    @classmethod
    def generate_bl_down(cls):
        h = randint(3, 5)
        crv = cls(h)
        crv.transform('hor_flip')
        return crv

    @classmethod
    def generate(cls, style=0):
        style_dict = {
            0: cls.generate_br_down,
            1: cls.generate_br_up,
            2: cls.generate_bl_down,
            3: cls.generate_bl_up,
        }
        style_num = len(style_dict)
        s = style % style_num
        return style_dict[s]()

    def __init__(self, h, coord=(0, 0), autooutline=True):

        true_h = h + 2
        true_w = self.set_true_width(h)

        Component.__init__(self, (true_w, true_h), coord=coord, autooutline=autooutline)

    @staticmethod
    def set_true_width(h):
        w = 2
        while h != 0:
            w += h
            h -= 1
        return w

    def outline(self, trim=False):
        return self.alt_outline(trim)

    def create(self):

        dim = self.w - 1
        mod = 1

        for y in range(self.h):
            if y < 1 or y == self.h - 1:
                continue

            for x in range(1, dim):
                self.add_point((x, y))

            dim -= mod
            mod += 1
