from component import Component
from random import *
                
                
class Rect(Component):

    @classmethod
    def generate_normal(cls):
        w = randint(3, 10)
        h = randint(3, 7)
        return cls((w, h))

    @classmethod
    def generate_long(cls):
        w = randint(5, 20)
        h = randint(3, 5)
        return cls((w, h))

    @classmethod
    def generate_peg(cls):
        w = randint(3, 4)
        h = randint(4, 7)
        return cls((w, h))

    @classmethod
    def generate_beam(cls):
        w = randint(5, 20)
        h = 3
        return cls((w, h))

    @classmethod
    def generate(cls, style=0):
        style_dict = {0: cls.generate_normal,
                      1: cls.generate_long,
                      2: cls.generate_peg,
                      3: cls.generate_beam
                      }
        style_num = len(style_dict)
        s = style % style_num
        return style_dict[s]()

    def __init__(self, (w, h)):
        
        Component.__init__(self, (w, h))
        
    def create(self):
    
        for y in range(self.h):
            for x in range(self.w):
                self.add_pixel((x, y))
                
                
class Square(Rect):

    @classmethod
    def generate(cls, style=0):
        w = randint(3, 10)
        return cls(w)

    def __init__(self, w):
        Rect.__init__(self, (w, w))


class _Angle(Component):

    @classmethod
    def generate(cls, style=0):
        w = randint(5, 10)
        return cls(w)

    # not a working component - base class for 45 degree
    # angle components

    def __init__(self, w, coord=(0, 0), m=1, b=0):

        self.m = m
        self.b = b

        Component.__init__(self, (w, w), coord=coord, autocreate=False)

    def create(self):

        for y in range(self.h):
            for x in range(self.w):
                if self.on_angle(x, y):
                    self.add_pixel((x, y))

    def on_angle(self, x, y):
        return False

    def line(self, x):
        return self.m*x + self.b


class AngleTopRight(_Angle):

    def __init__(self, w, coord=(0, 0), autooutline=True):

        _Angle.__init__(self, w, coord)
        self.create()
        if autooutline:
            self.outline()

    def on_angle(self, x, y):
        if self.line(x) <= y:
            return True
        else:
            return False


class AngleTopLeft(_Angle):

    def __init__(self, w, coord=(0, 0), autooutline=True):

        _Angle.__init__(self, w, coord, m=-1, b=w)
        self.create()
        if autooutline:
            self.outline()

    def on_angle(self, x, y):
        if self.line(x) <= y:
            return True
        else:
            return False


class AngleBottomRight(_Angle):

    def __init__(self, w, coord=(0, 0), autooutline=True):

        _Angle.__init__(self, w, coord, m=-1, b=w)
        self.create()
        if autooutline:
            self.outline()

    def on_angle(self, x, y):
        if self.line(x) >= y:
            return True
        else:
            return False


class AngleBottomLeft(_Angle):

    def __init__(self, w, coord=(0, 0), autooutline=True):

        _Angle.__init__(self, w, coord)
        self.create()
        if autooutline:
            self.outline()

    def on_angle(self, x, y):
        if self.line(x) >= y:
            return True
        else:
            return False


class Diamond(Component):

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