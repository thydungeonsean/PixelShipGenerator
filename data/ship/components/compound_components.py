from component import Component
from angles import *


class Diamond(Component):

    @classmethod
    def generate(cls, style=0):
        w = randint(4, 11)
        return cls(w)

    def __init__(self, w):
        Component.__init__(self, (w, w))

    def create(self):
        w = self.w / 2
        tr = Angle((w, w), coord=(w, 0), autooutline=False)
        br = Angle((w, w), coord=(w, w), autooutline=False)
        br.transform('clockwise')
        tl = Angle((w, w),  autooutline=False)
        tl.transform('counter_clockwise')
        bl = Angle((w, w), coord=(0, w), autooutline=False)
        bl.transform('clockwise')
        bl.transform('clockwise')

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

        w = self.w / 2
        tr = Angle((w, w), coord=(w, 0), autooutline=False)
        br = Angle((w, w), coord=(w, w), autooutline=False)
        br.transform('clockwise')
        tl = Angle((w, w),  autooutline=False)
        tl.transform('counter_clockwise')
        bl = Angle((w, w), coord=(0, w), autooutline=False)
        bl.transform('clockwise')
        bl.transform('clockwise')

        for component in (tl, tr, bl, br):

            self.add(component)

        self.outline(trim=True)


