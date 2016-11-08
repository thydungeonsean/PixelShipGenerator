

class Component(object):
    
    """ This is the base class for a ship
    component. It should not be directly created.
    Create() must be overwritten by subclass. This
    sets the initial value of the map
    """

    def __init__(self, (x, y), (w, h), autocreate=True, autooutline=True):
        
        self.map = [[0 for y in range(h)] for x in range(w)]
        self.w = w
        self.h = h
        
        self.x = x
        print str(x) + 'is the x'
        self.y = y
        
        self.points = set()

        if autocreate:
            self.create()
            if autooutline:
                self.outline()

    def create(self):
        pass

    def outline(self):

        # flood fill from edge of map to set a border or black
        # around component

        edge = self.get_edge_set()
        seen = set()

        while edge:
            next = set()
            for x, y in edge:
                seen.add((x, y))
                if self.map[x][y] == 1:
                    self.map[x][y] = -1
                elif self.map[x][y] == 0:
                    next.add((x, y))
            edge = self.get_next_edge(next, seen)

    def get_next_edge(self, next, seen):

        edge = set()

        for point in next:
            adj = self.get_adj(point)
            for p in adj:
                if p not in seen:
                    edge.add(p)
        return edge

    def get_adj(self, (x, y)):

        raw_adj = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        adj = set()
        for p in raw_adj:
            if self.is_on_map(p):
                adj.add(p)

        return adj

    def is_on_map(self, (x, y)):

        if 0 <= x < self.w and 0 <= y < self.h:
            return True
        else:
            return False

    def print_map(self):

        for y in range(self.h):
            line = ''
            for x in range(self.w):
                if self.map[x][y] == 0:
                    new = '  '
                elif self.map[x][y] == 1:
                    new = ' #'
                elif self.map[x][y] == -1:
                    new = ' -'
                line += new
            print line

    def get_edge_set(self):

        edge = set()

        for y in range(self.h):
            for x in range(self.w):
                if y == 0 or y == self.h - 1:
                    edge.add((x, y))
                elif x == 0 or x == self.w - 1:
                    edge.add((x, y))

        return edge

    # adds a component object's map to current map
    def add(self, component):

        sx = component.x
        sy = component.y
        w = component.w
        h = component.h

        print 'component stats'
        print sx, sy, w, h
        for y in range(h):
            for x in range(w):
                mx = sx + x
                my = sy + y
                c_value = component.map[x][y]
                if c_value != 0:
                    self.map[mx][my] = c_value

    def attach(self, ship):
        
        for x, y in self.points:
            x += self.x
            y += self.y
            ship.change_pixel((x, y), self.map[x][y])
            
    def place(self):
        pass
