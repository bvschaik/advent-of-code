import adventofcode
from collections import defaultdict

ADJACENT3 = []
for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            if not (x == 0 and y == 0 and z == 0):
                ADJACENT3.append((x, y, z))

ADJACENT4 = []
for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            for w in range(-1, 2):
                if not (x == 0 and y == 0 and z == 0 and w == 0):
                    ADJACENT4.append((x, y, z, w))

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(17)

    def reset(self):
        self.initial_state = []

    def input_line(self, line):
        self.initial_state.append(line)

    def solve1(self):
        active = set()
        neighbours = defaultdict(int)

        # Set up initial state
        for y, line in enumerate(self.initial_state):
            for x, c in enumerate(line):
                if c == '#':
                    active.add((x, y, 0))
                    for dx, dy, dz in ADJACENT3:
                        neighbours[(x+dx, y+dy, dz)] += 1

        for i in range(6):
            to_active = []
            to_inactive = []
            for a in active:
                n = neighbours[a]
                if n != 2 and n != 3:
                    to_inactive.append(a)
            for a in neighbours:
                if neighbours[a] == 3 and a not in active:
                    to_active.append(a)
            # Update for next round
            for a in to_active:
                active.add(a)
                for dx, dy, dz in ADJACENT3:
                    neighbours[(a[0]+dx, a[1]+dy, a[2]+dz)] += 1
            for a in to_inactive:
                active.remove(a)
                for dx, dy, dz in ADJACENT3:
                    neighbours[(a[0]+dx, a[1]+dy, a[2]+dz)] -= 1
        return str(len(active))

    def solve2(self):
        active = set()
        neighbours = defaultdict(int)

        # Set up initial state
        for y, line in enumerate(self.initial_state):
            for x, c in enumerate(line):
                if c == '#':
                    active.add((x, y, 0, 0))
                    for dx, dy, dz, dw in ADJACENT4:
                        neighbours[(x+dx, y+dy, dz, dw)] += 1

        for i in range(6):
            to_active = []
            to_inactive = []
            for a in active:
                n = neighbours[a]
                if n != 2 and n != 3:
                    to_inactive.append(a)
            for a in neighbours:
                if neighbours[a] == 3 and a not in active:
                    to_active.append(a)
            # Update for next round
            for a in to_active:
                active.add(a)
                for dx, dy, dz, dw in ADJACENT4:
                    neighbours[(a[0]+dx, a[1]+dy, a[2]+dz, a[3]+dw)] += 1
            for a in to_inactive:
                active.remove(a)
                for dx, dy, dz, dw in ADJACENT4:
                    neighbours[(a[0]+dx, a[1]+dy, a[2]+dz, a[3]+dw)] -= 1
        return str(len(active))

r = runner()

r.test('Sample 1', [
    '.#.',
    '..#',
    '###',
], '112', '848')

r.run()
