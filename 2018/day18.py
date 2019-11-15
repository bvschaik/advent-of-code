import re
from runner import runner

NONE = 4
OPEN = 0
TREE = 1
LUMBER = 2

def convert(x):
    if x == OPEN:
        return '.'
    elif x == TREE:
        return '|'
    elif x == LUMBER:
        return '#'
    else:
        return '?'

def from_char(x):
    if x == '.':
        return OPEN
    elif x == '|':
        return TREE
    else:
        return LUMBER

class day18(runner):
    def __init__(self):
        self.map = []

    def day(self):
        return 18

    def input(self, line):
        self.map.append(line)

    def solve1(self):
        grid = self.create_grid()

        for _ in range(10):
            (grid, _) = self.evolve(grid)

        return str(self.count_all(grid, TREE) * self.count_all(grid, LUMBER))

    def solve2(self):
        grid = self.create_grid()

        delta = 0
        delta_count = 0
        delta_index = None
        values = [0]
        while True:
            (grid, value) = self.evolve(grid)
            if delta and values[-delta] == value:
                delta_count += 1
                if delta_count == delta:
                    return str(values[delta_index + (1000000000 - delta_index) % delta])
            else:
                delta_index = self.find_last_index(values, value)
                if delta_index:
                    delta = len(values) - delta_index
                    delta_count = 1
                else:
                    delta = 0
                    delta_count = 0
            values.append(value)

    def find_last_index(self, values, value):
        for i in range(len(values) - 1, -1, -1):
            if values[i] == value:
                return i
        return None

    def create_grid(self):
        empty_row = [NONE] * (len(self.map[0]) + 2)
        return [empty_row] + [[NONE] + [from_char(x) for x in line] + [NONE] for line in self.map] + [empty_row]

    def evolve(self, grid):
        tree_count = 0
        lumber_count = 0

        max_y = len(grid) - 1
        max_x = len(grid[0]) - 1
        empty_row = [NONE] * (len(self.map[0]) + 2)
        new_grid = [empty_row]
        for y in range(1, max_y):
            new_row = [NONE]
            for x in range(1, max_x):
                current = grid[y][x]
                new_value = current
                if current == OPEN and self.count_adjacent(grid, x, y, TREE) >= 3:
                    new_value = TREE
                elif current == TREE and self.count_adjacent(grid, x, y, LUMBER) >= 3:
                    new_value = LUMBER
                elif current == LUMBER and (self.count_adjacent(grid, x, y, TREE) == 0 or self.count_adjacent(grid, x, y, LUMBER) == 0):
                    new_value = OPEN
                new_row.append(new_value)

                if new_value == TREE:
                    tree_count += 1
                elif new_value == LUMBER:
                    lumber_count += 1

            new_row.append(NONE)
            new_grid.append(new_row)
        new_grid.append(empty_row)
        return (new_grid, tree_count * lumber_count)

    def count_adjacent(self, grid, x, y, type):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx != 0 or dy != 0) and grid[y + dy][x + dx] == type:
                    count += 1
        return count

    def count_all(self, grid, type):
        count = 0
        for row in grid:
            for val in row:
                if val == type:
                    count += 1
        return count

    def debug(self, grid):
        for row in grid:
            for val in row:
                print(convert(val), end = '')
            print()

day18().test('Sample input', [
    '.#.#...|#.',
    '.....#|##|',
    '.|..|...#.',
    '..|#.....#',
    '#.#|||#|#|',
    '...#.||...',
    '.|....|...',
    '||...#|.#|',
    '|.||||..|.',
    '...#.|..|.',
], '1147')

day18().solve()
