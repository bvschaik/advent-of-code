import re
from runner import runner

class position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def distance_to_origin(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def translate(self, dx, dy, dz):
        return position(self.x + dx, self.y + dy, self.z + dz)

class nanobot:
    def __init__(self, x, y, z, r):
        self.pos = position(x, y, z)
        self.r = r

    def in_range(self, pos):
        return self.pos.distance_to(pos) <= self.r

class cube:
    def __init__(self, center, r, bots):
        self.center = center
        self.min_pos = position(center.x - r, center.y - r, center.z - r)
        self.max_pos = position(center.x + r - 1, center.y + r - 1, center.z + r - 1)
        self.r = r
        self.bots = list(filter(lambda b: self.intersects(b), bots))
        self.bots_in_range = len(self.bots)

    def intersects(self, bot):
        if self.r == 0:
            return bot.in_range(self.center)
        # Calculate minimum distance required to travel along each axis to
        # arrive at the bounding box. Sum to find the Manhattan distance.
        distance = (
            self.min_axis_dist(bot.pos.x, self.min_pos.x, self.max_pos.x) +
            self.min_axis_dist(bot.pos.y, self.min_pos.y, self.max_pos.y) +
            self.min_axis_dist(bot.pos.z, self.min_pos.z, self.max_pos.z))
        return distance <= bot.r

    def min_axis_dist(self, target, a_min, a_max):
        if target < a_min:
            return a_min - target
        elif target > a_max:
            return target - a_max
        else:
            return 0

    def split(self):
        if self.r == 0:
            return []
        new_r = self.r // 2
        low = -new_r if new_r > 0 else -1
        high = new_r
        cubes = [
            cube(self.center.translate(low, low, low), new_r, self.bots),
            cube(self.center.translate(low, low, high), new_r, self.bots),
            cube(self.center.translate(low, high, low), new_r, self.bots),
            cube(self.center.translate(low, high, high), new_r, self.bots),
            cube(self.center.translate(high, low, low), new_r, self.bots),
            cube(self.center.translate(high, low, high), new_r, self.bots),
            cube(self.center.translate(high, high, low), new_r, self.bots),
            cube(self.center.translate(high, high, high), new_r, self.bots)
        ]
        cubes.sort(key = lambda c: c.bots_in_range, reverse = True)
        return cubes

class day23(runner):
    def __init__(self):
        self.bots = []

    def day(self):
        return 23

    def input(self, line):
        m = re.match(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)', line)
        self.bots.append(nanobot(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    def solve1(self):
        max_bot = max(self.bots, key = lambda b: b.r)
        in_range = sum(1 for b in self.bots if max_bot.in_range(b.pos))
        return str(in_range)

    def solve2(self):
        self.max_bots = 0
        self.max_position = position(0, 0, 0)
        start_cube = cube(position(0, 0, 0), 2**30, self.bots)
        self.binary_search([start_cube])
        return str(self.max_position.distance_to_origin())

    def binary_search(self, cubes):
        for c in cubes:
            if c.bots_in_range > self.max_bots:
                # print("Searching cube %d %d %d %d" % (c.center.x, c.center.y, c.center.z, c.r))
                self.update_search_state(c)
                self.binary_search(c.split())

    def update_search_state(self, c):
        if c.r != 0 or c.bots_in_range < self.max_bots:
            return
        if c.bots_in_range > self.max_bots:
            # print("Updating min to %d" % c.bots_in_range)
            self.max_bots = c.bots_in_range
            self.max_position = c.center
        elif c.center.distance_to_origin() < self.max_position.distance_to_origin():
            self.max_position = c.center
            
day23().test('Sample input', [
    'pos=<0,0,0>, r=4',
    'pos=<1,0,0>, r=1',
    'pos=<4,0,0>, r=3',
    'pos=<0,2,0>, r=1',
    'pos=<0,5,0>, r=3',
    'pos=<0,0,3>, r=1',
    'pos=<1,1,1>, r=1',
    'pos=<1,1,2>, r=1',
    'pos=<1,3,1>, r=1',
], '7')

day23().test('Sample input part 2', [
    'pos=<10,12,12>, r=2',
    'pos=<12,14,12>, r=2',
    'pos=<16,12,12>, r=4',
    'pos=<14,14,14>, r=6',
    'pos=<50,50,50>, r=200',
    'pos=<10,10,10>, r=5',
], '6', '36')

day23().solve()
