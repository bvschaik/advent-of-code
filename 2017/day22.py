import adventofcode
from collections import defaultdict

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(22)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data.append(line)

    def solve1(self):
        grid = defaultdict(bool)
        for y, row in enumerate(self.data):
            for x, c in enumerate(row):
                grid[(x, y)] = True if c == '#' else False

        direction = 0
        pos = (len(self.data[0]) // 2, len(self.data[1]) // 2)

        infected = 0
        for n in range(10000):
            if grid[pos]:
                direction = (direction + 1) % 4
            else:
                direction = (direction - 1) % 4
                infected += 1
            grid[pos] = not grid[pos]
            pos = (pos[0] + DIRECTIONS[direction][0], pos[1] + DIRECTIONS[direction][1])

        return str(infected)

    def solve2(self):
        grid = defaultdict(int)
        for y, row in enumerate(self.data):
            for x, c in enumerate(row):
                grid[(x, y)] = INFECTED if c == '#' else CLEAN

        direction = 0
        pos = (len(self.data[0]) // 2, len(self.data[1]) // 2)

        infected = 0
        for n in range(10000000):
            state = grid[pos]
            if state == CLEAN:
                direction = (direction - 1) % 4
            elif state == WEAKENED:
                infected += 1
            elif state == INFECTED:
                direction = (direction + 1) % 4
            elif state == FLAGGED:
                direction = (direction + 2) % 4
            grid[pos] = (state + 1) % 4
            pos = (pos[0] + DIRECTIONS[direction][0], pos[1] + DIRECTIONS[direction][1])

        return str(infected)

r = runner()
r.run()
