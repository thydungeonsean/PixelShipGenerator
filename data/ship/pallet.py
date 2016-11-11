import components.basic_hull as bh
from random import *


class Pallet(object):

    def __init__(self):

        #self.component_list = [(bh.Rect, 0), (bh.Rect, 1), (bh.Square, 0),
                               # (bh.AngleBottomRight, 0), (bh.Diamond, 0),
                               # (bh.AngleTopRight, 0), (bh.AngleBottomLeft, 0),
                               # (bh.AngleTopLeft, 0)]
        self.component_list = [(bh.Rect, 3), (bh.Rect, 1), (bh.Rect, 2), (bh.Diamond, 0)]

    def get_component(self):

        generator, style = choice(self.component_list)
        component = generator.generate(style)

        return component
