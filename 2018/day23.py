import re
from runner import runner

class nanobot:
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.neighbours = set()

    def distance_to(self, n):
        return abs(self.x - n.x) + abs(self.y - n.y) + abs(self.z - n.z)

    def __repr__(self):
        return str.format("nanobot(%d, %d, %d)" % (self.x, self.y, self.z))

class day23(runner):
    def __init__(self):
        self.bots = []

    def day(self):
        return 23

    def input(self, line):
        m = re.match(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)', line)
        self.bots.append(nanobot(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    def solve1(self):
        max_bot = max(self.bots, key = lambda b: b.radius)
        in_range = 0
        for bot in self.bots:
            if bot.distance_to(max_bot) <= max_bot.radius:
                in_range += 1
        return str(in_range)

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

day23().solve()
