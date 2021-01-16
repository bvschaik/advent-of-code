import adventofcode
from collections import defaultdict

NORTH = (-1, 0, 1)
NORTHEAST = (0, -1, 1)
NORTHWEST = (-1, 1, 0)
SOUTH = (1, 0, -1)
SOUTHEAST = (1, -1, 0)
SOUTHWEST = (0, 1, -1)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(11)

    def reset(self):
        self.steps = []

    def input_line(self, line):
        self.steps = line.split(',')

    def solve1(self):
        directions = defaultdict(int)
        for s in self.steps:
            directions[s] += 1
        delta_n = directions['n'] - directions['s']
        delta_ne = directions['ne'] - directions['sw']
        delta_nw = directions['nw'] - directions['se']
        coord = (
            NORTH[0] * delta_n + NORTHEAST[0] * delta_ne + NORTHWEST[0] * delta_nw,
            NORTH[1] * delta_n + NORTHEAST[1] * delta_ne + NORTHWEST[1] * delta_nw,
            NORTH[2] * delta_n + NORTHEAST[2] * delta_ne + NORTHWEST[2] * delta_nw,
        )
        return str(self.distance(coord))

    def solve2(self):
        max_dist = 0
        coord = [0, 0, 0]
        for s in self.steps:
            if s == 'n':
                direction = NORTH
            elif s == 'ne':
                direction = NORTHEAST
            elif s == 'nw':
                direction = NORTHWEST
            elif s == 's':
                direction = SOUTH
            elif s == 'se':
                direction = SOUTHEAST
            elif s == 'sw':
                direction = SOUTHWEST
            coord[0] += direction[0]
            coord[1] += direction[1]
            coord[2] += direction[2]
            dist = self.distance(coord)
            if dist > max_dist:
                max_dist = dist
        return str(max_dist)

    def distance(self, coord):
        return max(map(abs, coord))

r = runner()
r.run()
