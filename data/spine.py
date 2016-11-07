

class Spine(object):

    """ Spine is owned by Ship. It's created based on Frame.
    Spine is a set of coordinates that are attachable for components.
    """

    def __init__(self, frame):

        self.frame = frame

        self.spine = self.build_spine()

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
            for x in range(int(zone.w*.25), int(zone.w*.75)):
                spine.add((x+zone.x1, y+zone.y1))
        elif zone.h > zone.w:
            x = int(zone.w / 2)
            for y in range(int(zone.h * .25), int(zone.h * .75)):
                spine.add((x+zone.x1, y+zone.y1))
        else:
            x = int(zone.w / 2)
            for y in range(int(zone.h * .25), int(zone.h * .75)):
                spine.add((x + zone.x1, y + zone.y1))
            y = int(zone.h / 2)
            for x in range(int(zone.w * .25), int(zone.w * .75)):
                spine.add((x + zone.x1, y + zone.y1))

        return spine
