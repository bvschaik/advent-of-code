import adventofcode
import math

def list_asteroids(directions, direction_asteroids):
    dir_index = 0
    while directions:
        cur_dir = directions[dir_index]
        if not cur_dir in direction_asteroids:
            del directions[dir_index]
            continue
        asteroids = direction_asteroids[cur_dir]
        yield asteroids[0]
        asteroids.pop(0)
        if not asteroids:
            del direction_asteroids[cur_dir]
            del directions[dir_index]
        else:
            dir_index += 1
        if dir_index >= len(directions):
            dir_index = 0

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(10)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data.append(line)

    def solve1(self):
        width = len(self.data[0])
        height = len(self.data)
        asteroids = dict()
        for y in range(height):
            for x in range(width):
                if self.data[y][x] == '#':
                    asteroids[(x, y)] = 0

        for y in range(height):
            for x in range(-width + 1, width + 1):
                if ((x == 0 and y > 0) or (x > 0 and y == 0) or (x != 0 and y != 0)) and math.gcd(x, y) == 1:
                    self.process_vector(x, y, width, height, asteroids)

        max_value = max(asteroids.values())
        self.best_asteroid = next(a[0] for a in asteroids.items() if a[1] == max_value)
        return str(max_value)

    def process_vector(self, dx, dy, width, height, asteroids):
        for y in range(0, height):
            for x in range(0, width):
                if dx >= 0:
                    if x - dx < 0 or y - dy < 0:
                        self.process_line(x, y, dx, dy, width, height, asteroids)
                else:
                    if x - dx >= width or y - dy < 0:
                        self.process_line(x, y, dx, dy, width, height, asteroids)

    def process_line(self, x, y, dx, dy, width, height, asteroids):
        prev_asteroid = None
        point = (x, y)
        while point[0] >= 0 and point[0] < width and point[1] < height:
            if point in asteroids:
                if prev_asteroid:
                    asteroids[prev_asteroid] += 1
                    asteroids[point] += 1
                prev_asteroid = point
            point = (point[0] + dx, point[1] + dy)

    def solve2(self):
        width = len(self.data[0])
        height = len(self.data)
        max_width = max(self.best_asteroid[0], width - self.best_asteroid[0]) + 1
        max_height = max(self.best_asteroid[1], height - self.best_asteroid[1]) + 1
        all_directions = self.get_all_directions(max_width, max_height)

        direction_asteroids = dict()
        for d in all_directions:
            asteroids = self.get_asteroids(d[0], d[1], self.best_asteroid[0], self.best_asteroid[1], width, height)
            if asteroids:
                direction_asteroids[d] = asteroids

        for i, ast in enumerate(list_asteroids(all_directions, direction_asteroids)):
            if i == 199:
                return str(ast[0] * 100 + ast[1])
        
        return None

    def get_all_directions(self, max_width, max_height):
        directions = []
        for x in range(1, max_width):
            for y in range(1, max_height):
                if math.gcd(x, y) == 1:
                    directions.append((x, y))
        directions.sort(key = lambda p: p[1] / p[0])
        all_directions = []
        all_directions.append((0, -1))
        all_directions += reversed(list(map(lambda p: (p[0], -p[1]), directions)))
        all_directions.append((1, 0))
        all_directions += directions
        all_directions.append((0, 1))
        all_directions += reversed(list(map(lambda p: (-p[0], p[1]), directions)))
        all_directions.append((-1, 0))
        all_directions += list(map(lambda p: (-p[0], -p[1]), directions))
        return all_directions

    def get_asteroids(self, dx, dy, ox, oy, width, height):
        p = (ox + dx, oy + dy)
        asteroids = []
        while p[0] >= 0 and p[0] < width and p[1] >= 0 and p[1] < height:
            if self.data[p[1]][p[0]] == '#':
                asteroids.append(p)
            p = (p[0] + dx, p[1] + dy)
        return asteroids

r = runner()

r.test('Sample', [
    '.#..#',
    '.....',
    '#####',
    '....#',
    '...##',
], '8')

r.run()
