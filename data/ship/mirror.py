from pixel_map import PixelMap


class Mirror(PixelMap):

    @classmethod
    def get_mirror(cls, ship, orientation):
        return cls(ship)

    def __init__(self, ship):

        w = ship.w
        h = ship.h

        PixelMap.__init__(self, (w, h))
        self.ship = ship
        self.ship_points = set()


    def run(self):
        self.run_vertical_a()

    def run_vertical_a(self):

        self.ship_points = self.get_ship_points()
        line = self.get_vertical_split('a')

    def get_ship_points(self):

        points = set()
        points.update(self.ship.points)
        points.update(self.ship.edges)

        return points

    def over_write(self):

        self.ship.points = self.points
        self.ship.edges = self.edges
        self.ship.map = self.map

    def get_vertical_split(self, variant):

        x_tot = 0
        y_tot = 0
        length = len(self.ship_points)

        for (x, y) in list(self.ship_points):
            x_tot += x
            y_tot += y

        x_avg = x_tot / length
        y_avg = y_tot / length

        

