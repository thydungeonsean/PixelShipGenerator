from random import *
from spine import Spine


class Frame(object):

    """ Frame is owned by ship. It represents set of points
    within the ship's map that most of the pixels will fall
    within.
    """

    """
    Frame.layout contains preset parameters for the creation of a set of zones.

    Keywords:

    horizontal magnitude
    Long - 1/8*w - 7/8*w
    Med - 1/4*w - 3/4*w
    Short - 1/3*w - 2/3*w
    Skinny - 2/5*w - 3/5*w

    vertical magnitude
    Tall - 1/8*w - 7/8*w
    Med - 1/4*w - 3/4*w
    Short - 1/3*w - 2/3*w
    Squat - 2/5*w - 3/5*w

    horizontal placement
    Left
    Right
    RandX

    vertical placement
    Top
    High
    Low
    Bot
    RandY

    ex: ('Long', 'Short', 'Top')
    - horizontal placement defaults to center
    - vertical defaults to center

    """

    layout_parser = {
        'LongX': .125,
        'LongW': .75,
        'MedX': .25,
        'MedW': .5,
        'ShortX': .333,
        'ShortW': .333,
        'SkinnyX': .4,
        'SkinnyW': .2,
        'TallY': .125,
        'TallH': .75,
        'MedY': .25,
        'MedH': .5,
        'ShortY': .333,
        'ShortH': .333,
        'SquatY': .4,
        'SquatH': .2
    }

    default = (('Med', 'Med'), )
    # prefabricated zone layouts
    layout = {'rect': (('Long', 'Short'), ),
              'square': (('Long', 'Tall'), ),
              'donut': (('Long', 'Squat', 'Top'),
                        ('Long', 'Squat', 'Bot'),
                        ('Skinny', 'Tall', 'Right'),
                        ('Skinny', 'Tall', 'Left')),
              'cross': (('Long', 'Squat'),
                        ('Skinny', 'Med')),
              'right_cross': (('Long', 'Squat'),
                              ('Skinny', 'Med', 'RandX')),
              'left_cross': (('Long', 'Squat'),
                             ('Skinny', 'Med', 'Left')),
              'rand_cross': (('Long', 'Squat'),
                             ('Skinny', 'Med', 'Right')),
              'claw': (('Long', 'Squat', 'High'),
                       ('Long', 'Squat', 'Low'),
                       ('Skinny', 'Med', 'Right')),
              'talon': (('Long', 'Squat', 'Top'),
                        ('Med', 'Squat'),
                        ('Skinny', 'Short', 'Right', 'High')),
              'left_corner': (('Long', 'Short'),
                              ('Skinny', 'Med', 'Left', 'Low')),
              'right_corner': (('Long', 'Short'),
                               ('Skinny', 'Med', 'Right', 'Low')),
              }

    max_zones = 5

    layout_hor = ('Long', 'Med', 'Short', 'Skinny')
    layout_ver = ('Tall', 'Med', 'Short', 'Squat')
    layout_x = ('Left', 'Right', 'RandX')
    layout_y = ('Top', 'Bot', 'High', 'Low', 'RandY')

    @classmethod
    def random(cls, ship):
        return cls(ship, 'random')

    @classmethod
    def rand_premade(cls, ship):
        return cls(ship, choice(cls.layout.keys()))

    @classmethod
    def preselected(cls, ship, layout):
        return cls(ship, layout)

    def __init__(self, ship, layout='default'):

        self.w = ship.w
        self.h = ship.h

        self.layout = layout

        # one or more rectangular areas that constitutes the frame
        self.zones = self.load_zone_layout(layout)

        # count of unique points that are within the frame
        self.zone_capacity = self.get_capacity()

        self.spine = Spine(self)

    def load_zone_layout(self, key):

        zones = []

        if key == 'default':
            layout = Frame.default
        elif key == 'random':
            layout = self.generate_random_layout()
        else:
            layout = Frame.layout[key]

        for zone in layout:
            topleft, dimensions = self.parse_zone(zone)
            new_zone = Zone(topleft, dimensions)
            zones.append(new_zone)

        return zones

    def parse_zone(self, zone):

        x = int(Frame.layout_parser[zone[0]+'X'] * self.w)
        w = int(Frame.layout_parser[zone[0]+'W'] * self.w)
        y = int(Frame.layout_parser[zone[1]+'Y'] * self.h)
        h = int(Frame.layout_parser[zone[1]+'H'] * self.h)

        if len(zone) == 2:
            return (x, y), (w, h)

        xMargin = x
        yMargin = y

        case = {
            'Left': xMargin * -.5,
            'Right': xMargin * .5,
            'RandX': randint(int(xMargin*-.8), int(xMargin*.8)),
            'Top': yMargin * -.8,
            'High': yMargin * -.5,
            'Low': yMargin * .5,
            'Bot': yMargin * .8,
            'RandY': randint(int(yMargin*-.8), int(yMargin*.8))
        }

        xmod = ('Left', 'Right', 'RandX')
        ymod = ('Top', 'High', 'Low', 'Bot', 'RandY')

        for keyword in zone[2:]:

            if keyword in xmod:
                x += int(case[keyword])
            elif keyword in ymod:
                y += int(case[keyword])

        return (x, y), (w, h)

    def generate_random_layout(self):

        layout = []

        for z in range(randint(1, Frame.max_zones)):
            new = self.generate_random_zone()
            layout.append(new)

        return tuple(layout)

    def generate_random_zone(self):

        zone = [choice(Frame.layout_hor), choice(Frame.layout_ver)]
        if randint(0, 1) == 1:
            zone.append(choice(Frame.layout_x))
        if randint(0, 1) == 1:
            zone.append(choice(Frame.layout_y))

        return tuple(zone)

    def get_capacity(self):

        count = 0

        for y in range(self.h):
            for x in range(self.w):
                if self.is_in_frame((x, y)):
                    count += 1

        return count

    def is_frame_full(self):
        return False

    def is_in_frame(self, point):

        for zone in self.zones:
            if zone.is_in(point):
                return True

        return False

    def point_in_frame(self):

        while True:
            x = randint(0, self.w-1)
            y = randint(0, self.h-1)
            if self.is_in_frame((x, y)):
                return x, y


class Zone(object):

    """ Zone is owned by Frame.
    A frame is a collection of one or more zones.
    Zone describes a rectangular area within the ship
    map.
    """

    def __init__(self, (x, y), (w, h)):

        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.w = w
        self.h = h
        self.size = x * y

    def is_in(self, (x, y)):

        if self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2:
            return True
        else:
            return False
