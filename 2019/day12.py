import adventofcode
import math
import re

class jupiter_moon:
    def __init__(self, x, y, z):
        self.px = x
        self.py = y
        self.pz = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def apply_gravity(self, moon):
        if self.px < moon.px:
            self.vx += 1
        elif self.px > moon.px:
            self.vx -= 1
        if self.py < moon.py:
            self.vy += 1
        elif self.py > moon.py:
            self.vy -= 1
        if self.pz < moon.pz:
            self.vz += 1
        elif self.pz > moon.pz:
            self.vz -= 1

    def move(self):
        self.px += self.vx
        self.py += self.vy
        self.pz += self.vz

    def energy(self):
        return (abs(self.px) + abs(self.py) + abs(self.pz)) * (abs(self.vx) + abs(self.vy) + abs(self.vz))

    def state(self):
        return (self.px, self.py, self.pz, self.vx, self.vy, self.vz)

    def __repr__(self):
        return str.format('p=(%d, %d, %d) v=(%d, %d, %d)' % (self.px, self.py, self.pz, self.vx, self.vy, self.vz))

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(12)

    def reset(self):
        self.moons = []

    def input_line(self, line):
        m = re.match(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line)
        self.moons.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))

    def solve1(self):
        moons = list(map(lambda m: jupiter_moon(m[0], m[1], m[2]), self.moons))

        for _ in range(0, 1000):
            for m in moons:
                for n in moons:
                    if m != n:
                        m.apply_gravity(n)
            for m in moons:
                m.move()

        return str(sum(map(lambda m: m.energy(), moons)))

    def solve2(self):
        moons = list(map(lambda m: jupiter_moon(m[0], m[1], m[2]), self.moons))

        states = []
        for _ in range(0, 300000):
            for m in moons:
                for n in moons:
                    if m != n:
                        m.apply_gravity(n)
            for m in moons:
                m.move()
            states.append(moons[0].state() + moons[1].state() + moons[2].state() + moons[3].state())

        periods = set()
        for n in range(24):
            period = self.find_period(states, n)
            periods.add(period)
            print("Period for", n, "is", self.find_period(states, n))

        lcm = 1
        for p in periods:
            lcm = abs(lcm * p) // math.gcd(lcm, p)
        return str(lcm)

    def find_period(self, states, index):
        for i, s in enumerate(states):
            if i and states[0][index] == s[index]:
                found = True
                for j in range(min(i, len(states) - i)):
                    if states[j][index] != states[i + j][index]:
                        found = False
                        break
                if found:
                    return i
        return -1

r = runner()

# r.test('Sample', [
#     '<x=-1, y=0, z=2>',
#     '<x=2, y=-10, z=-7>',
#     '<x=4, y=-8, z=8>',
#     '<x=3, y=5, z=-1>',
# ], None, '2772')

r.run()
