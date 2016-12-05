from pixel_map import PixelMap


class Mirror(PixelMap):

    @classmethod
    def get_mirror(cls, ship, orientation):
        return cls(ship, orientation)

    def __init__(self, ship, orientation):

        w = ship.w
        h = ship.h

        PixelMap.__init__(self, (w, h))
        self.ship = ship

        self.orientation = orientation
        self.run_function = self.assign_run_function()

    def assign_run_function(self):

        func_dict = {
            'vertical_a': self.run_vertical_a,
            'vertical_b': self.run_vertical_b,
            'horizontal_a': self.run_horizontal_a,
            'horizontal_b': self.run_horizontal_b,
            'quad_': self.run_quad
        }

        if self.orientation.startswith('quad'):
            key = 'quad_'
        else:
            key = self.orientation

        return func_dict[key]

    def run(self):
        self.run_function()

        self.over_write()
        self.ship.check_connected()

    def run_vertical_a(self):

        line = self.get_vertical_split()

        rows = range(line+1)
        columns = range(self.w)
        self.grab_map(rows, columns, self.ship, line, 'ver')

    def run_vertical_b(self):

        line = self.get_vertical_split()

        rows = range(line, self.h)
        columns = range(self.w)
        self.grab_map(rows, columns, self.ship, line, 'ver')

    def run_horizontal_a(self):

        line = self.get_horizontal_split()

        rows = range(self.h)
        columns = range(line+1)
        self.grab_map(rows, columns, self.ship, line, 'hor')

    def run_horizontal_b(self):

        line = self.get_horizontal_split()

        rows = range(self.h)
        columns = range(line, self.w)
        self.grab_map(rows, columns, self.ship, line, 'hor')

    def run_quad(self):

        tag = self.orientation.lstrip('quad_')

        x_line, y_line = self.get_avg_lines()

        quad_arg_dict = {
            'tl': (range(y_line+1), range(x_line+1)),
            'tr': (range(y_line+1), range(x_line, self.w)),
            'bl': (range(y_line, self.h), range(x_line+1)),
            'br': (range(y_line, self.h), range(x_line, self.w))
        }

        args = quad_arg_dict[tag]

        rows = args[0]
        columns = args[1]
        self.grab_map(rows, columns, self.ship, x_line, 'hor')

        rows = args[0]
        columns = range(self.w)
        self.grab_map(rows, columns, self, y_line, 'ver')

    def grab_map(self, rows, columns, target_map, line, axis):

        if axis == 'ver':
            add_reflected_point = self.add_vertical_reflected_point
        elif axis == 'hor':
            add_reflected_point = self.add_horizontal_reflected_point

        edges = []

        for y in rows:
            for x in columns:
                value = target_map.map[x][y]
                self.add_point((x, y), value)
                if value != 0:
                    edges.append((x, y))

        # TODO have something that tests if this is a valid reflection
        # don't want single pixel ships making it through too much
        final_points = self.trim_outliers(edges)

        #final_points = ship_points
        for (x, y) in final_points:
            value = self.map[x][y]
            add_reflected_point((x, y), value, line)

    def get_ship_points(self):

        points = self.ship.get_total_points()

        return points

    def over_write(self):

        self.ship.points = self.points
        self.ship.edges = self.edges
        self.ship.map = self.map

    def get_vertical_split(self):

        return self.get_avg_lines()[1]

    def get_horizontal_split(self):

        return self.get_avg_lines()[0]

    def get_avg_lines(self):

        ship_points = self.get_ship_points()

        x_tot = 0
        y_tot = 0
        length = len(ship_points)

        for (x, y) in list(ship_points):
            x_tot += x
            y_tot += y

        x_avg = x_tot / length
        y_avg = y_tot / length

        return x_avg, y_avg

    def add_vertical_reflected_point(self, (x, y), value, line):

        direction = 'up'
        if y <= line:
            direction = 'down'

        diff = abs(line - y)

        if direction == 'up':
            new_y = line - diff
        elif direction == 'down':
            new_y = line + diff

        self.add_point((x, new_y), value)

    def add_horizontal_reflected_point(self, (x, y), value, line):

        direction = 'left'
        if x <= line:
            direction = 'right'

        diff = abs(line - x)

        if direction == 'left':
            new_x = line - diff
        elif direction == 'right':
            new_x = line + diff

        self.add_point((new_x, y), value)

    def trim_outliers(self, points):
        
        initial_points = set(points)
        valid_points = set()

        for x, y in points:
            
            adj = self.get_adj((x, y), diag=True)
            
            for ax, ay in adj:
                if self.map[ax][ay] >= 1:
                    valid_points.add((x, y))
                    break

        remove_points = list(initial_points.difference(valid_points))
        
        for point in remove_points:
            self.trim_point(point)

        return list(valid_points)

