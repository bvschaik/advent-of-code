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

    def solve2(self):
        # Find pairs of nodes that have at least one point which is in range of both nodes
        for ia, a in enumerate(self.bots):
            for ib in range(ia + 1, len(self.bots)):
                b = self.bots[ib]
                if a.distance_to(b) <= a.radius + b.radius and a is not b:
                    a.neighbours.add(b)
                    b.neighbours.add(a)

        # Assuming: A and B, A and C, and B and C are neighbours: there's a spot where we are in range of all 3
        # Find largest 'clique' of inter-connected nodes
        max_clique = self.bron_kerbosch(set(), set(self.bots), set())

        # The overlapping region closest to the origin is the maximum distance to the origin
        # of a node minus its radius: if there were a point farther away, then its distance from
        # the origin would be larger
        origin = nanobot(0, 0, 0, 0)
        answer = max(map(lambda x: x.distance_to(origin) - x.radius, max_clique))

        return str(answer)

    def bron_kerbosch(self, r, p, x, max_size = 0):
        if not p and not x:
            # print(len(r), max_size)
            return r
        if len(p) + len(x) + len(r) <= max_size:
            # short-circuit
            return set()
        pivot = max(p | x, key = lambda n: len(n.neighbours))
        non_neighbours = p - pivot.neighbours
        pp = set(p)
        xx = set(x)
        max_clique = set()
        for v in non_neighbours:
            clique = self.bron_kerbosch(r | {v}, pp & v.neighbours, xx & v.neighbours, len(max_clique))
            if len(clique) > len(max_clique):
                max_clique = clique
            pp.remove(v)
            xx.add(v)
        return max_clique

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
