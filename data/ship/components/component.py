

class Component(object):
    
    """ This is the base class for a ship
    component. It should not be directly created.
    Create() must be overwritten by subclass. This
    sets the initial value of the map
    """

    def __init__(self, (x, y), (w, h), autocreate=True, autooutline=True):

        self.w = w
        self.h = h
        
        self.x = x
        self.y = y
        
        # maybe this is the problem - had x and y as var names for list builder
        # and they were before assigning proper attributes - renamed mx, my
        self.map = [[0 for my in range(h)] for mx in range(w)]
        
        self.points = set()

        if autocreate:
            self.create()
            if autooutline:
                self.outline()

    def create(self):
        pass

    def add_pixel(self, (x, y), value=1):

        self.map[x][y] = value
        self.points.add((x, y))

    def outline(self, trim=False):
    
        outline = set()
        for x, y in self.points:

            if y == 0 or y == self.h-1 or x == 0 or x == self.w-1:
                outline.add((x, y))
                continue

            adj = self.get_adj((x, y))
            for ax, ay in adj:
                if self.map[ax][ay] == 0:
                    outline.add((x, y))
                    break
                    
        for px, py in outline:
            self.map[px][py] = -1

        if trim:
            self.trim_outline(outline)

    def trim_outline(self, outline):

        trim = set()

        for x, y in outline:
            adj = self.get_adj((x, y))
            next_to_pixel = False
            for ax, ay in adj:
                if self.map[ax][ay] == 1:
                    next_to_pixel = True
                    break
            if not next_to_pixel:
                trim.add((x, y))

        for tx, ty in trim:
            self.map[tx][ty] = 0
            self.points.remove((tx, ty))
 
    def get_adj(self, (x, y)):

        raw_adj = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        adj = set()
        for p in raw_adj:
            if self.is_on_map(p):
                adj.add(p)

        return adj
       
    ##################################################################
    # realized this floodfill to outline was needlessly complicated
    # and would also fail to outline internal details
    def flood_outline(self):

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
        
    def get_edge_set(self):

        edge = set()

        for y in range(self.h):
            for x in range(self.w):
                if y == 0 or y == self.h - 1:
                    edge.add((x, y))
                elif x == 0 or x == self.w - 1:
                    edge.add((x, y))

        return edge
    ####################################################################

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

    # adds a component object's map to current map
    def add(self, component):

        sx = component.x
        sy = component.y
        w = component.w
        h = component.h

        for y in range(h):
            for x in range(w):
                mx = sx + x
                my = sy + y
                c_value = component.map[x][y]
                if c_value != 0:
                    self.add_pixel((mx, my), value=c_value)

    def attach(self, ship):
        
        for x, y in self.points:
            x += self.x
            y += self.y
            ship.change_pixel((x, y), self.map[x][y])
            
    def place(self):
        pass
        # select a start position on ship map
        # check if attached
        # check if not overlapping
        # if those pass, check if in frame
        # needs methods to move position intelligently to meet conditions

