import components.basic_hull as bh
import components.compound_components as ch
from random import *


class Palette(object):

    basic = ((bh.Rect, 0), (bh.Rect, 1), (bh.Rect, 3), (bh.Square, 0))
    connector = ((bh.Rect, 2), (bh.Square, 1))
    angles = ((bh.AngleTopLeft, 0), (bh.AngleTopRight, 0), (bh.AngleBottomLeft, 0),
              (bh.AngleBottomRight, 0), (ch.Diamond, 0))
    special = ((ch.Circle, 0),)

    def __init__(self):

        # self.component_list = [(bh.Rect, 0), (bh.Rect, 1), (bh.Square, 0),
                               # (bh.AngleBottomRight, 0), (bh.Diamond, 0),
                               # (bh.AngleTopRight, 0), (bh.AngleBottomLeft, 0),
                               # (bh.AngleTopLeft, 0)]
        #self.component_list = [(bh.Rect, 3), (bh.Rect, 1), (bh.Rect, 2), (ch.Circle, 0)]

        self.basic = randint(2, 6)
        self.connector = randint(1, 2)
        self.angles = randint(0, 1)
        self.special = randint(0, 1)

        self.component_list = self.set_component_list()

    def get_component(self):

        generator, style = choice(self.component_list)
        component = generator.generate(style)

        return component

    def set_component_list(self):

        c_list = []

        for i in range(self.basic):
            c_list.append(choice(Palette.basic))

        for i in range(self.connector):
            c_list.append(choice(Palette.connector))

        for i in range(self.angles):
            c_list.append(choice(Palette.angles))

        for i in range(self.special):
            c_list.append(choice(Palette.special))

        return c_list

