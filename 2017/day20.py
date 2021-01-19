import adventofcode
import math
import re
from collections import defaultdict

def solve_quadratic(a, b, c):
    solutions = []
    if a == 0:
        return solutions
    d = b * b - 4 * a * c
    if d < 0:
        return solutions
    sq_d = math.isqrt(d)
    if sq_d * sq_d != d:
        return solutions
    s1 = -b - sq_d
    s2 = -b + sq_d
    if s1 % (2 * a) == 0 and s1 // (2 * a) > 0:
        solutions.append(s1 // (2 * a))
    if s2 % (2 * a) == 0 and s2 // (2 * a) > 0:
        solutions.append(s2 // (2 * a))
    return solutions

def check_quadratic(a, b, c, n):
    return a * n * n + b * n + c == 0

class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def add(self, vector):
        return vec3(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def sub(self, vector):
        return vec3(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def mul(self, vector):
        return vec3(self.x * vector.x, self.y * vector.y, self.z * vector.z)

    def times(self, value):
        return vec3(self.x * value, self.y * value, self.z * value)

    def square(self):
        return vec3(self.x * self.x, self.y * self.y, self.z * self.z)

    def is_square(self):
        if self.x < 0 or self.y < 0 or self.z < 0:
            return False
        rx = math.isqrt(self.x)
        ry = math.isqrt(self.y)
        rz = math.isqrt(self.z)
        return rx * rx == self.x and ry * ry == self.y and rz * rz == self.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return str.format('(%d,%d,%d)' % (self.x, self.y, self.z))

class particle:
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    def advance(self):
        self.v = self.v.add(self.a)
        self.p = self.p.add(self.v)

    def advance_multiple(self, times):
        return self.p.add(self.v.times(times)).add(self.a.times(times * (times + 1) // 2))

    def at(self, time):
        return self.p.add(self.v.times(time)).add(self.a.times(time * (time + 1) // 2))

    def sort_key(self):
        return (self.a.distance(), self.p.distance())

    def collision_time(self, other):
        # Position at time n = P + n * V + 1/2 * n * (n+1) * A
        # To calculate collision time, we need to solve this formula for x, y, z for two particles s, t:
        # 1/2 * As * n^2 + (1/2 * As + Vs) * n + Ps = 1/2 * At * n^2 + (1/2 * At + Vt) * n + Pt
        # This reduces to a standard quadratic formula, solvable using the ABC formula:
        # (As - At) * n^2 + (As - At + 2 * (Vs - Vt)) * n + 2 * (Ps - Pt) = 0
        delta_ax = self.a.x - other.a.x
        delta_vx = self.v.x - other.v.x
        delta_px = self.p.x - other.p.x
        solutions = solve_quadratic(delta_ax, delta_ax + 2 * delta_vx, 2 * delta_px)
        if solutions:
            delta_a = self.a.sub(other.a)
            delta_v = self.v.sub(other.v)
            delta_p = self.p.sub(other.p)
            for n in sorted(solutions):
                if (check_quadratic(delta_a.y, delta_a.y + 2 * delta_v.y, 2 * delta_p.y, n) and
                    check_quadratic(delta_a.z, delta_a.z + 2 * delta_v.z, 2 * delta_p.z, n)):
                    return n
        return None

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(20)

    def reset(self):
        self.particles = []

    def input_line(self, line):
        m = re.match(r'p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>', line)
        self.particles.append(particle(
            vec3(int(m.group(1)), int(m.group(2)), int(m.group(3))),
            vec3(int(m.group(4)), int(m.group(5)), int(m.group(6))),
            vec3(int(m.group(7)), int(m.group(8)), int(m.group(9)))
        ))

    def solve1(self):
        (id, particle) = min(enumerate(self.particles), key = lambda p: p[1].sort_key())
        return str(id)

    def solve2(self):
        max_n = len(self.particles)
        collisions = defaultdict(set)
        for a in range(max_n):
            pa = self.particles[a]
            for b in range(a + 1, max_n):
                pb = self.particles[b]
                time = self.particles[a].collision_time(self.particles[b])
                if time:
                    key = (time, pa.at(time).to_tuple())
                    collisions[key].add(a)
                    collisions[key].add(b)
        destroyed = set()
        for key in sorted(collisions):
            particles = collisions[key] - destroyed
            if len(particles) > 1:
                destroyed |= particles
        return str(len(self.particles) - len(destroyed))

r = runner()

r.run()
