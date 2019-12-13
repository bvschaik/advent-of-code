import adventofcode
import math
import re

class jupiter_moon:
    def __init__(self, x, y, z):
        self.start_position = [x, y, z]
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]

    def apply_gravity(self, moon):
        if self.position[0] < moon.position[0]:
            self.velocity[0] += 1
            moon.velocity[0] -= 1
        elif self.position[0] > moon.position[0]:
            self.velocity[0] -= 1
            moon.velocity[0] += 1
        if self.position[1] < moon.position[1]:
            self.velocity[1] += 1
            moon.velocity[1] -= 1
        elif self.position[1] > moon.position[1]:
            self.velocity[1] -= 1
            moon.velocity[1] += 1
        if self.position[2] < moon.position[2]:
            self.velocity[2] += 1
            moon.velocity[2] -= 1
        elif self.position[2] > moon.position[2]:
            self.velocity[2] -= 1
            moon.velocity[2] += 1

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[2] += self.velocity[2]

    def energy(self):
        return sum(map(abs, self.position)) * sum(map(abs, self.velocity))

    def __repr__(self):
        return str.format('p=%s v=%s' % (self.position, self.velocity))

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
            for i in range(1, len(moons)):
                for j in range(i):
                    moons[i].apply_gravity(moons[j])
            for m in moons:
                m.move()

        return str(sum(map(lambda m: m.energy(), moons)))

    def solve2(self):
        moons = list(map(lambda m: jupiter_moon(m[0], m[1], m[2]), self.moons))

        period_x = 0
        period_y = 0
        period_z = 0
        counter = 0
        while period_x == 0 or period_y == 0 or period_z == 0:
            for i in range(1, len(moons)):
                for j in range(i):
                    moons[i].apply_gravity(moons[j])
            for m in moons:
                m.move()
            counter += 1

            if not period_x and self.is_start_pos(moons, 0):
                period_x = counter
                print("Period x is", period_x)
            if not period_y and self.is_start_pos(moons, 1):
                period_y = counter
                print("Period y is", period_y)
            if not period_z and self.is_start_pos(moons, 2):
                period_z = counter
                print("Period z is", period_z)

        return str(self.lcm(period_x, self.lcm(period_y, period_z)))

    def lcm(self, a, b):
        return abs(a * b) // math.gcd(a, b)

    def is_start_pos(self, moons, index):
        for m in moons:
            if m.velocity[index] != 0:
                return False
            if m.position[index] != m.start_position[index]:
                return False
        return True

r = runner()

r.test('Sample', [
    '<x=-1, y=0, z=2>',
    '<x=2, y=-10, z=-7>',
    '<x=4, y=-8, z=8>',
    '<x=3, y=5, z=-1>',
], None, '2772')

r.run()
