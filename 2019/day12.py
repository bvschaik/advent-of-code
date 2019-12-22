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

class jupiter_moon_axis:
    def __init__(self, n):
        self.start_position = n
        self.position = n
        self.velocity = 0

    def apply_gravity(self, moon):
        if self.position < moon.position:
            self.velocity += 1
            moon.velocity -= 1
        elif self.position > moon.position:
            self.velocity -= 1
            moon.velocity += 1

    def move(self):
        self.position += self.velocity

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
        moons_x = list(map(lambda m: jupiter_moon_axis(m[0]), self.moons))
        moons_y = list(map(lambda m: jupiter_moon_axis(m[1]), self.moons))
        moons_z = list(map(lambda m: jupiter_moon_axis(m[2]), self.moons))

        period_x = self.find_period(moons_x)
        period_y = self.find_period(moons_y)
        period_z = self.find_period(moons_z)

        # print(period_x, period_y, period_z)
        return str(self.lcm(period_x, self.lcm(period_y, period_z)))

    def find_period(self, moons):
        counter = 0
        while counter == 0 or not all(map(lambda m: m.velocity == 0 and m.position == m.start_position, moons)):
            for i in range(1, len(moons)):
                for j in range(i):
                    moons[i].apply_gravity(moons[j])
            for m in moons:
                m.move()
            counter += 1
        return counter

    def lcm(self, a, b):
        return abs(a * b) // math.gcd(a, b)

r = runner()

r.test('Sample', [
    '<x=-1, y=0, z=2>',
    '<x=2, y=-10, z=-7>',
    '<x=4, y=-8, z=8>',
    '<x=3, y=5, z=-1>',
], None, '2772')

r.test('Sample 2', [
    '<x=-8, y=-10, z=0>',
    '<x=5, y=5, z=10>',
    '<x=2, y=-7, z=3>',
    '<x=9, y=-8, z=-3>',
], None, '4686774924')

r.run()
