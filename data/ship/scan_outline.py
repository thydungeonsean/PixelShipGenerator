from pixel_map import PixelMap
from ..constants import *
from random import choice


class ScanOutline(PixelMap):

    def __init__(self, ship):

        self.ship = ship
        w = self.ship.w + 4
        h = self.ship.h + 4
        PixelMap.__init__(self, (w, h), colorkey=True)
        self.fill_color = WHITE

        self.silhouette = set()

        self.set_scan_outline()

        self.trace = self.set_trace()

        self.update_image()

    def set_scan_outline(self):

        self.set_silhouette()

        inner_edge = self.flood_find_outer_edge()
        self.add_points(inner_edge)
        final_edge = self.flood_find_outer_edge()
        self.add_points(final_edge)
        self.clear_edges(inner_edge)

        self.remove_silhouette()

    def add_points(self, points):
        for point in points:
            self.add_point(point)

    def clear_edges(self, edge):
        for x, y in edge:
            self.trim_point((x, y))

    def position(self, (x, y)):
        self.rect.topleft = (x-scale(2), y-scale(2))

    def flood_find_outer_edge(self):

        queue = [(0, 0)]
        edge = set()
        visited = {(0, 0)}

        while queue:

            queue = self.flood(queue, edge, visited)

        return edge

    def flood(self, queue, edge, visited):

        next_queue = set()

        for qx, qy in queue:

            visited.add((qx, qy))
            neighbours = self.get_adj((qx, qy))

            for (nx, ny) in neighbours:
                if self.map[nx][ny] != 0:
                    edge.add((qx, qy))
                    continue
                elif (nx, ny) not in visited:
                    next_queue.add((nx, ny))

        return list(next_queue)

    def set_silhouette(self):

        points = self.ship.get_total_points(return_type='list')

        for (x, y) in points:
            value = self.ship.map[x][y]
            nx = x+2
            ny = y+2
            self.add_point((nx, ny), value)
            self.silhouette.add((nx, ny))

    def remove_silhouette(self):

        for point in self.silhouette:
            self.trim_point(point)

    def get_adj_line_points(self, point):

        adj = self.get_adj(point, diag=True)
        line = []

        for ax, ay in adj:
            if self.map[ax][ay] != 0:
                line.append((ax, ay))

        return line

    def set_trace(self):

        # pointlist = self.get_total_points(return_type='list')
        # for p in pointlist:
        #     self.draw_dot(p, col=YELLOW)
        # pygame.display.update()

        start = self.get_topleft()

        queue = [start]
        visited = {start}

        step = 0

        trace = {}

        while queue:

            trace[step] = set()
            for point in queue:
                trace[step].add(point)
                visited.add(point)

            #     self.draw_dot(point)
            # pygame.display.update()
            #
            # if pygame.event.wait().type == KEYDOWN:
            #     pass

            step += 1

            queue = self.get_next_queue(queue, visited)

        return trace

    def get_next_queue(self, old_queue, visited):

        next = set()

        for point in old_queue:
            adj = self.get_adj_line_points(point)
            for a_point in adj:
                if a_point not in visited:
                    next.add(a_point)

        return list(next)

    def get_topleft(self):

        points = self.get_total_points(return_type='list')

        low_point = choice(points)
        low_val = low_point[0] + low_point[1]

        for x, y in points:
            if x+y < low_val:
                low_val = x+y
                low_point = (x, y)

        return low_point

    def animate_trace(self):

        screen = pygame.display.get_surface()

        dot = pygame.Surface((SCALE, SCALE))
        dot1 = dot.copy()
        dot1.fill((240, 240, 255))
        dot2 = dot.copy()
        dot2.fill((150, 200, 230))
        dot3 = dot.copy()
        dot3.fill(BLUE)
        r = dot.get_rect()

        for i in range(len(self.trace)+20):

            if i < len(self.trace):
                self.draw_points(self.trace[i], dot1, r, screen)

            if 9 < i < len(self.trace)+10:
                self.draw_points(self.trace[i-10], dot2, r, screen)

            if 19 < i < len(self.trace)+20:
                self.draw_points(self.trace[i-20], dot3, r, screen)

            pygame.display.update()
            pygame.time.delay(8)

    def draw_points(self, points, dot, r, screen):

        for x, y in points:
            r.topleft = (x * SCALE + 6, y * SCALE + 6)
            screen.blit(dot, r)
