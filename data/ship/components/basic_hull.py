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
        w = randint(5, 15)
        h = randint(3, 5)
        return cls((w, h))

    @classmethod
    def generate_peg(cls):
        w = randint(3, 4)
        h = randint(4, 9)
        return cls((w, h))

    @classmethod
    def generate_beam(cls):
        w = randint(5, 15)
        h = 3
        return cls((w, h))

    @classmethod
    def generate_tall(cls):
        w = randint(3, 6)
        h = randint(6, 12)
        return cls((w, h))

    @classmethod
    def generate(cls, style=0):
        style_dict = {0: cls.generate_normal,
                      1: cls.generate_long,
                      2: cls.generate_peg,
                      3: cls.generate_beam,
                      4: cls.generate_tall
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
    def generate_brick(cls):
        w = randint(3, 5)
        return cls(w)

    @classmethod
    def generate_square(cls):
        w = randint(5, 8)
        return cls(w)

    @classmethod
    def generate(cls, style=0):
        style_dict = {0: cls.generate_square,
                      1: cls.generate_brick
                      }
        style_num = len(style_dict)
        s = style % style_num
        return style_dict[s]()

    def __init__(self, w):
        Rect.__init__(self, (w, w))
