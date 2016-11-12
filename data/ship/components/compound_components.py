from component import Component
from basic_hull import *


class Diamond(Component):

    @classmethod
    def generate(cls, style=0):
        w = randint(2, 7)
        return cls(w)

    def __init__(self, w):
        end_w = w * 2-1
        Component.__init__(self, (end_w, end_w))

    def create(self):

        w = self.w/2 + 1
        tl = AngleTopLeft(w, coord=(0, 0), autooutline=False)
        tr = AngleTopRight(w, coord=(w-1, 0), autooutline=False)
        bl = AngleBottomLeft(w, coord=(0, w-1),  autooutline=False)
        br = AngleBottomRight(w, coord=(w-1, w-1), autooutline=False)

        for component in (tl, tr, bl, br):

            self.add(component)

        self.outline(trim=True)


class Circle(Component):

    @classmethod
    def generate(cls, style=0):
        w = randint(5, 11)
        return cls(w)

    def __init__(self, w):

        Component.__init__(self, (w, w))

    def create(self):

        w = self.w/2
        tl = AngleTopLeft(w, coord=(0, 0), autooutline=False)
        tr = AngleTopRight(w, coord=(w-1, 0), autooutline=False)
        bl = AngleBottomLeft(w, coord=(0, w-1),  autooutline=False)
        br = AngleBottomRight(w, coord=(w-1, w-1), autooutline=False)

        for component in (tl, tr, bl, br):

            self.add(component)

        self.outline(trim=True)


