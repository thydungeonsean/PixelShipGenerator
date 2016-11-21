from random import *


class ComponentPlacer(object):

    directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))

    def __init__(self, ship, component):

        self.ship = ship
        self.component = component

        self.visited_positions = set()

        self.move_log = []
        self.move_dict = {}

        self.vector = None
        self.vector_log = []

        self.reversed_once = False

    # log recording functions
    @property
    def current_position(self):
        if len(self.move_log) < 1:
            return None
        return self.move_log[-1]

    @property
    def current_state(self):
        if self.current_position is None:
            return None
        return self.move_dict[self.current_position]

    @property
    def previous_position(self):
        if len(self.move_log) > 1:
            return self.move_log[-2]
        return None

    @property
    def previous_state(self):
        if self.previous_position is None:
            return None
        return self.move_dict[self.previous_position]

    def record(self, pos, state):

        self.move_log.append(pos)
        self.move_dict[pos] = state
        self.visited_positions.add(pos)

    # start point chooosers
    def get_start_point(self, start):
        if start == 0:
            return self.get_start_point_in_frame()
        elif start == 1:
            return self.get_start_point_on_edge()

    def get_start_point_in_frame(self):

        c = self.component

        ix, iy = self.ship.frame.point_in_frame()
        xvar = c.w / 2
        yvar = c.h / 2
        ix += randint(-xvar, xvar)
        iy += randint(-yvar, yvar)

        return ix, iy

    def get_start_point_on_edge(self):

        if not self.ship.edges:
            return self.get_start_point_in_frame()

        c = self.component

        ix, iy = choice(tuple(self.ship.edges))
        xvar = c.w / 2
        yvar = c.h / 2
        ix += randint(-xvar, xvar)
        iy += randint(-yvar, yvar)

        return ix, iy

    # main placement algorithm
    def place(self, start=randint(0, 1)):

        # if this is first placement of component, we generate a start point
        if not self.move_log:
            return self.get_start_point(start)

        current_state = self.current_state
        previous_state = self.previous_state



        # if component is not connected to ship or spine, we try to shift it to the center of
        # the map hopefully to connect
        if current_state == 'unconnected':
            if previous_state == 'unconnected' or previous_state is None:
                self.move_towards_center()
                return self.move_on_vector()
            elif not self.reversed_once:  # we went from connected to unconnected - no good, find new solution
                self.reverse_vector()
                self.reversed_once = True
                return self.move_on_vector()
            else:
                self.reversed_once = False
                self.set_random_vector()
                return self.move_on_vector()

        # if we are connected but overlapping, try and move so that we reduce amount overlapping
        # at beginning, pick a random direction
        if previous_state is None or previous_state == 'unconnected':
            self.set_random_vector()
            return self.move_on_vector()

        if previous_state <= current_state:
            # keep going same way
            return self.move_on_vector()

        if previous_state > current_state:
            self.set_new_vector()
            return self.move_on_vector()

    # vector tools
    def set_new_vector(self):

        previous = set(self.vector_log)
        diff = tuple(set(ComponentPlacer.directions).difference(previous))
        if not diff:
            self.set_random_vector()
        else:
            choice(diff)

    def reverse_vector(self):
        new = []
        for i in self.vector:
            if i == 1:
                n = -1
            elif i == 0:
                n = 0
            elif i == -1:
                n = 1
            new.append(n)
        new_vector = tuple(new)
        self.change_vector(new_vector)

    def move_on_vector(self):
        dx, dy = self.vector
        cx, cy = self.current_position
        return dx + cx, dy + cy

    def set_random_vector(self):
        vector = choice(ComponentPlacer.directions)
        self.update_vector(vector)

    def update_vector(self, vector):
        self.vector_log = []
        self.vector = vector

    def change_vector(self, new):
        self.vector_log.append(self.vector)
        self.vector = new

    def move_towards_center(self):

        cx, cy = self.current_position
        if cx >= self.component.w / 2:
            dx = -1
        else:
            dx = 1
        if cy >= self.component.h / 2:
            dy = -1
        else:
            dy = 1
        self.update_vector((dx, dy))
