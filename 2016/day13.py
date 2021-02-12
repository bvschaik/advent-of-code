import adventofcode

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(13)

    def reset(self):
        self.seed = 0

    def input_line(self, line):
        self.seed = int(line)

    def solve1(self):
        visited = set()
        positions = {(1, 1)}
        distance = 0
        while positions:
            new_positions = set()
            for x, y in positions:
                if x == 31 and y == 39:
                    return str(distance)
                for dx, dy in DIRECTIONS:
                    if self.is_open(x + dx, y + dy):
                        np = (x + dx, y + dy)
                        if np not in visited:
                            new_positions.add(np)
                            visited.add(np)
            distance += 1
            positions = new_positions

    def solve2(self):
        visited = set()
        positions = {(1, 1)}
        for dist in range(50):
            new_positions = set()
            for x, y in positions:
                for dx, dy in DIRECTIONS:
                    if self.is_open(x + dx, y + dy):
                        np = (x + dx, y + dy)
                        if np not in visited:
                            new_positions.add(np)
                            visited.add(np)
            positions = new_positions
        return str(len(visited))

    def is_open(self, x, y):
        if x < 0 or y < 0:
            return False
        value = x*x + 3*x + 2*x*y + y + y*y + self.seed
        return self.parity(value) == 0

    def parity(self, value):
        value ^= value >> 16
        value ^= value >> 8
        value ^= value >> 4
        value ^= value >> 2
        value ^= value >> 1
        return value & 1

r = runner()
r.run()
