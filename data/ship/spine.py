

class Spine(object):

    """ Spine is owned by Ship. It's created based on Frame.
    Spine is a set of coordinates that are attachable for components.
    """

    def __init__(self, frame):

        self.frame = frame

        self.points = self.build_spine()

    def build_spine(self):

        spine = set()

        for zone in self.frame.zones:
            zone_spine = self.get_zone_spine(zone)
            spine.update(zone_spine)

        return spine

    @staticmethod
    def get_zone_spine(zone):

        spine = set()

        if zone.w > zone.h:
            y = int(zone.h/2)
            spine.update(Spine.get_horizontal_line(zone, y))
        elif zone.h > zone.w:
            x = int(zone.w / 2)
            spine.update(Spine.get_vertical_line(zone, x))
        else:  # for square zone
            x = int(zone.w / 4)
            spine.update(Spine.get_vertical_line(zone, x))
            x = int(zone.w * .75)
            spine.update(Spine.get_vertical_line(zone, x))
            y = int(zone.h / 4)
            spine.update(Spine.get_horizontal_line(zone, y))
            y = int(zone.h * .75)
            spine.update(Spine.get_horizontal_line(zone, y))

        return spine

    @staticmethod
    def get_horizontal_line(zone, y):

        line = set()

        x1 = int(zone.w*.125)
        x2 = int(zone.w*.825)

        for x in range(x1, x2):
            line.add((x+zone.x1, y+zone.y1))

        return line

    @staticmethod
    def get_vertical_line(zone, x):

        line = set()

        y1 = int(zone.h*.125)
        y2 = int(zone.h*.825)

        for y in range(y1, y2):
            line.add((x+zone.x1, y+zone.y1))

        return line
