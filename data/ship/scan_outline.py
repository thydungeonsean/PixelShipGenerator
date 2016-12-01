from pixel_map import PixelMap
from ..constants import *


class ScanOutline(PixelMap):

    def __init__(self, ship):

        self.ship = ship
        w = self.ship.w + 4
        h = self.ship.h + 4
        PixelMap.__init__(self, (w, h), colorkey=True)
        self.fill_color = WHITE

        self.set_scan_outline()

        self.update_image()

    def set_scan_outline(self):

        inner_edge = self.flood_find_outer_edge(p_map=self.ship)
        self.add_points(inner_edge)
        final_edge = self.flood_find_outer_edge()
        self.add_points(final_edge)
        self.clear_edges(inner_edge)

    def add_points(self, points):
        for point in points:
            self.add_point(point)

    def clear_edges(self, edge):
        for x, y in edge:
            self.trim_point((x, y))

    def position(self, (x, y)):
        self.rect.topleft = (x, y)
        self.rect.topleft = (x+scale(2), y+scale(2))

    def flood_find_outer_edge(self, p_map=None):

        queue = [(0, 0)]
        edge = set()
        visited = {(0, 0)}

        while queue:

            queue = self.flood(queue, edge, visited, p_map=p_map)

        return edge

    def flood(self, queue, edge, visited, p_map=None):

        mod = 2
        if p_map is None:
            p_map = self
            mod = 0

        next_queue = set()

        for qx, qy in queue:
            p_map_x = qx + mod
            p_map_y = qy + mod

            visited.add((qx, qy))
            neighbours = p_map.get_adj((p_map_x, p_map_y))

            for (nx, ny) in neighbours:
                if p_map.map[nx][ny] != 0:
                    edge.add((qx, qy))
                    continue
                elif (nx-mod, ny-mod) not in visited:
                    next_queue.add((nx-mod, ny-mod))

        return list(next_queue)
