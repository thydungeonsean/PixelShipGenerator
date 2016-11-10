from component import Component
from random import *
                
                
class Rect(Component):

    def __init__(self, (x, y), (w, h)):
        
        Component.__init__(self, (x, y), (w, h))
        
    def create(self):
    
        for y in range(self.h):
            for x in range(self.w):
                self.add_pixel((x, y))
                
                
class Square(Rect):

    def __init__(self, (x, y), (w, h)):
        w = min((w, h))
        Rect.__init__(self, (x, y), (w, w))


class _Angle(Component):

    # not a working component - base class for 45 degree
    # angle components

    def __init__(self, (x, y), (w, h), m=1, b=0):

        self.m = m
        self.b = b

        Component.__init__(self, (x, y), (w, h), autocreate=False)

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

    def __init__(self, (x, y), (w, h), autooutline=True):

        _Angle.__init__(self, (x, y), (w, h))
        self.create()
        if autooutline:
            self.outline()

    def on_angle(self, x, y):
        if self.line(x) <= y:
            return True
        else:
            return False


class AngleTopLeft(_Angle):

    def __init__(self, (x, y), (w, h), autooutline=True):

        _Angle.__init__(self, (x, y), (w, h), m=-1, b=h)
        self.create()
        if autooutline:
            self.outline()

    def on_angle(self, x, y):
        if self.line(x) <= y:
            return True
        else:
            return False


class AngleBottomRight(_Angle):

    def __init__(self, (x, y), (w, h), autooutline=True):

        _Angle.__init__(self, (x, y), (w, h), m=-1, b=h)
        self.create()
        if autooutline:
            self.outline()

    def on_angle(self, x, y):
        if self.line(x) >= y:
            return True
        else:
            return False


class AngleBottomLeft(_Angle):

    def __init__(self, (x, y), (w, h), autooutline=True):

        _Angle.__init__(self, (x, y), (w, h))
        self.create()
        if autooutline:
            self.outline()

    def on_angle(self, x, y):
        if self.line(x) >= y:
            return True
        else:
            return False


class Diamond(Component):

    def __init__(self, (x, y), (w, h)):

        Component.__init__(self, (x, y), (w, h))

    def create(self):
        sub_w = self.w/2
        sub_h = self.h/2
        tl = AngleTopLeft((0, 0), (sub_w, sub_h), autooutline=False)
        tr = AngleTopRight((sub_w-1, 0), (sub_w, sub_h), autooutline=False)
        bl = AngleBottomLeft((0, sub_h-1), (sub_w, sub_h), autooutline=False)
        br = AngleBottomRight((sub_w-1, sub_h-1), (sub_w, sub_h), autooutline=False)

        for component in (tl, tr, bl, br):

            self.add(component)

        self.outline(trim=True)
