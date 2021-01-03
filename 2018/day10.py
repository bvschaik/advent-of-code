import adventofcode
import re

infinite = 10000000

class star:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __repr__(self):
        return str.format("star(x = %d, y = %d, dx = %d, y = %d)" % (self.x, self.y, self.dx, self.dy))

    def position_at(self, time):
        return (self.x + time * self.dx, self.y + time * self.dy)

    def time_until_positive(self):
        if self.x < 0 and self.y < 0:
            return max(-int(self.x / self.dx), -int(self.y / self.dy))
        elif self.x < 0:
            return -int(self.x / self.dx)
        elif self.y < 0:
            return -int(self.y / self.dy)
        else:
            return 0

    def time_until_negative(self):
        time_x = time_y = infinite
        if self.x >= 0 and self.dx < 0:
            time_x = -int(self.x / self.dx)
        if self.y >= 0 and self.dy < 0:
            time_y = -int(self.y / self.dy)
        return min(time_x, time_y)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(10)

    def reset(self):
        self.stars = []

    def input_line(self, line):
        m = re.match(r'position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>', line)
        self.stars.append(star(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    def solve1(self):
        # The message will be shown when all stars are close together, i.e. when the size of the constellation is smallest
        # The constellation is smallest when the points are close together,
        # so find the point where two lines in opposite directions cross
        positive_line = next(filter(lambda p: p.dx > 0 and p.dy > 0, self.stars))
        negative_line = next(filter(lambda p: p.dx < 0 and p.dy < 0, self.stars))

        # find t where Pos(t) = Neg(t), or: Px + t * Pdx == Nx + t * Ndx -> t * Pdx - t * Ndx = Nx - Px -> t = (Nx - Px) / (Pdx - Ndx)
        approx_time = int((negative_line.x - positive_line.x) / (positive_line.dx - negative_line.dx))
        if self.constellation_size(approx_time) > self.constellation_size(approx_time + 1):
            min_time = self.find_smallest_constellation_size(approx_time, +1)
        else:
            min_time = self.find_smallest_constellation_size(approx_time, -1)
        self.print_constellation(min_time)
        return str(min_time)

    def find_smallest_constellation_size(self, time, delta):
        next_time = time + delta
        size = self.constellation_size(time)
        next_size = self.constellation_size(next_time)
        while next_size < size:
            time = next_time
            next_time = time + delta
            size = next_size
            next_size = self.constellation_size(next_time)
        return time

    def constellation_size(self, time):
        positions = set(map(lambda p: p.position_at(time), self.stars))
        min_x = min(positions, key = lambda p: p[0])[0]
        max_x = max(positions, key = lambda p: p[0])[0]
        min_y = min(positions, key = lambda p: p[1])[1]
        max_y = max(positions, key = lambda p: p[1])[1]
        return max_y - min_y + max_x - min_x

    def print_constellation(self, time):
        positions = set(map(lambda p: p.position_at(time), self.stars))
        min_x = min(positions, key = lambda p: p[0])[0]
        max_x = max(positions, key = lambda p: p[0])[0]
        min_y = min(positions, key = lambda p: p[1])[1]
        max_y = max(positions, key = lambda p: p[1])[1]

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in positions:
                    print('#', end = '')
                else:
                    print('.', end = '')
            print()

    def solve2(self):
        # Solution to part 2 (time to wait) is already printed by part 1
        pass

r = runner()
r.test('Sample input', [
    'position=< 9,  1> velocity=< 0,  2>',
    'position=< 7,  0> velocity=<-1,  0>',
    'position=< 3, -2> velocity=<-1,  1>',
    'position=< 6, 10> velocity=<-2, -1>',
    'position=< 2, -4> velocity=< 2,  2>',
    'position=<-6, 10> velocity=< 2, -2>',
    'position=< 1,  8> velocity=< 1, -1>',
    'position=< 1,  7> velocity=< 1,  0>',
    'position=<-3, 11> velocity=< 1, -2>',
    'position=< 7,  6> velocity=<-1, -1>',
    'position=<-2,  3> velocity=< 1,  0>',
    'position=<-4,  3> velocity=< 2,  0>',
    'position=<10, -3> velocity=<-1,  1>',
    'position=< 5, 11> velocity=< 1, -2>',
    'position=< 4,  7> velocity=< 0, -1>',
    'position=< 8, -2> velocity=< 0,  1>',
    'position=<15,  0> velocity=<-2,  0>',
    'position=< 1,  6> velocity=< 1,  0>',
    'position=< 8,  9> velocity=< 0, -1>',
    'position=< 3,  3> velocity=<-1,  1>',
    'position=< 0,  5> velocity=< 0, -1>',
    'position=<-2,  2> velocity=< 2,  0>',
    'position=< 5, -2> velocity=< 1,  2>',
    'position=< 1,  4> velocity=< 2,  1>',
    'position=<-2,  7> velocity=< 2, -2>',
    'position=< 3,  6> velocity=<-1, -1>',
    'position=< 5,  0> velocity=< 1,  0>',
    'position=<-6,  0> velocity=< 2,  0>',
    'position=< 5,  9> velocity=< 1, -2>',
    'position=<14,  7> velocity=<-2,  0>',
    'position=<-3,  6> velocity=< 2, -1>'
], '3')

r.run()
