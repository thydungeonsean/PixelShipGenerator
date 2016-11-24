from pixel_map import PixelMap
from random import choice


class ShipConnector(PixelMap):
    @staticmethod
    def get_chunk_dict(m):

        chunk_dict = {}

        chunk_id = 0

        for y in range(m.h):
            for x in range(m.w):
                if m.map[x][y] == 0:
                    continue
                try:
                    chunk_dict[(x, y)]
                except KeyError:  # only try flood filling if it's not part of a chunk already
                    chunk_id += 1
                    ShipConnector.flood_chunk(m, (x, y), chunk_dict, chunk_id)

        return chunk_dict, chunk_id

    @staticmethod
    def flood_chunk(m, (x, y), dict, tag):

        dict[(x, y)] = (tag, m.map[x][y])

        queue = [(x, y)]

        complete = False

        while not complete:

            queue = ShipConnector.flood(m, queue, dict, tag)

            if not queue:
                complete = True

    @staticmethod
    def flood(m, queue, dict, tag):

        next_queue = []

        for point in queue:

            neighbours = m.get_adj(point)

            for p in neighbours:
                x, y = p
                if m.map[x][y] == 0:
                    continue
                try:
                    dict[p]
                except KeyError:
                    dict[p] = (tag, m.map[x][y])
                    next_queue.append(p)

        return next_queue

    def __init__(self, parent, chunk_dict, num):

        PixelMap.__init__(self, (parent.w, parent.h))

        self.parent = parent
        self.copy(parent)

        self.chunk_dict = chunk_dict
        self.num = num
        self.chunk_ids = range(1, num + 1)

        self.chunks = self.get_chunks()
        self.centers = self.get_chunk_centers()

    def other_chunk_ids(self, current):
        others = []
        for n in self.chunk_ids:
            if n not in current:
                others.append(n)
        return others

    def connect_chunks(self):

        # while unconnected:
        # find nearest 2 chunks to connect
        # increment the chunks towards one another until they touch
        # merge chunks
        # check if there are more chunks
        # repeat until all one chunk

        self.print_map()

        connected = False
        while not connected:
            print 'connecting'
            chunk1, chunk2 = self.get_two_chunks(self.centers)

            intersected = False
            while not intersected:
                print 'moving together'
                intersected = self.move_chunks_together(chunk1, chunk2)

            print 'intersected'
            self.save_points()
            self.reset_chunks()

            if self.num == 1:
                print 'fully connected'
                connected = True

    def save_points(self):

        self.new_map()

        for n in self.chunk_ids:
            for point, value in self.chunks[n]:
                self.add_point(point, value)

    def reset_chunks(self):

        self.chunk_dict, self.num = self.get_chunk_dict(self)
        self.chunk_ids = range(1, self.num + 1)
        self.chunks = self.get_chunks()
        self.centers = self.get_chunk_centers()
        print self.num
        self.print_map()

    def get_chunk_centers(self):

        centers = {}

        for n in self.chunk_ids:
            centers[n] = self.get_center(self.chunks[n])
            print centers[n]

        return centers

    def get_center(self, chunk):

        tot_x = 0
        tot_y = 0
        points = set()

        for (x, y), value in chunk:
            points.add((x, y))
            tot_x += x
            tot_y += y
        avg_x = tot_x / len(chunk)
        avg_y = tot_y / len(chunk)

        if (avg_x, avg_y) in points:
            return avg_x, avg_y

        closest = {}
        for (x, y), value in chunk:
            v = abs(x - avg_x) + abs(y - avg_y)
            closest[v] = (x, y)
        low_key = min(closest.keys())

        return closest[low_key]

    def get_chunks(self):

        chunks = {}
        for n in self.chunk_ids:
            chunks[n] = []

        for point, (id, value) in self.chunk_dict.items():
            chunks[id].append((point, value))

        return chunks

    def get_two_chunks(self, centers):

        ids = self.chunk_ids

        chunk1 = choice(ids)
        ax, ay = centers[chunk1]

        nearest = {}

        for n in ids:
            if n == chunk1:
                continue

            bx, by = centers[n]
            dist = abs(ax - bx) + abs(ay - by)

            nearest[dist] = n

        low_key = min(nearest.keys())
        chunk2 = nearest[low_key]

        return chunk1, chunk2

    def extract_points(self, chunk):
        points = set()
        for point, value in chunk:
            points.add(point)

        return points

    def move_chunks_together(self, a, b):

        for c1, c2 in ((a, b), (b, a)):

            for axis in ('x', 'y'):

                self.move_chunk((c1, c2), axis)

                set1 = self.extract_points(self.chunks[c1])
                set2 = self.extract_points(self.chunks[c2])

                if set1.intersection(set2):  # if there is overlap between the chunks, they are connected
                    intersect = True
                else:
                    intersect = False

                if intersect:
                    return True

                for n in self.other_chunk_ids((c1, c2)):
                    setn = self.extract_points(self.chunks[n])
                    if set1.intersection(setn):
                        return True

        return False

    def move_chunk(self, (a, b), axis):

        ax, ay = self.centers[a]
        bx, by = self.centers[b]

        if axis == 'x':
            if ax > bx:
                move = (-1, 0)
            elif ax < bx:
                move = (1, 0)
            else:
                return
        elif axis == 'y':
            if ay > by:
                move = (0, -1)
            elif ay < by:
                move = (0, 1)
            else:
                return

        moved = []

        for (x, y), value in self.chunks[a]:
            new = x + move[0], y + move[1]
            moved.append((new, value))

        new_center = ax + move[0], ay + move[1]

        self.centers[a] = new_center
        self.chunks[a] = moved
