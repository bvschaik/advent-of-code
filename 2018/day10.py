import re
from runner import runner

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

class day10(runner):
    def __init__(self):
        self.stars = []

    def day(self):
        return 10

    def input(self, line):
        m = re.match(r'position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>', line)
        self.stars.append(star(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    def solve1(self):
        # find smallest T where every point is positive in both x and y
        start_time = max(map(lambda p: p.time_until_positive(), self.stars))
        # find largest T where every point is still positive in both x and y
        end_time = min(map(lambda p: p.time_until_negative(), self.stars))

        # find time where constellation is smallest
        min_time = min(range(start_time, end_time + 1), key = lambda t: self.constellation_size(t))
        self.print_constellation(min_time)
        return str(min_time)

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


day10().test('Sample input', [
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

day10().solve()
