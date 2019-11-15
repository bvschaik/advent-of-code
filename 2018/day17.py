import re
from runner import runner

SAND = 0
CLAY = 8
FLOWING = 1
SETTLED = 4

def convert(x):
    if x == SAND:
        return '.'
    elif x == CLAY:
        return '#'
    elif x == FLOWING:
        return '|'
    elif x == SETTLED:
        return '~'
    else:
        return '?'

class vein:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

class day17(runner):
    def __init__(self):
        self.veins = []

    def day(self):
        return 17

    def input(self, line):
        m = re.match(r"x=(\d+), y=(\d+)\.\.(\d+)", line)
        if m:
            x = int(m.group(1))
            y1 = int(m.group(2))
            y2 = int(m.group(3))
            self.veins.append(vein(x, x, y1, y2))
        else:
            m = re.match(r"y=(\d+), x=(\d+)\.\.(\d+)", line)
            if m:
                y = int(m.group(1))
                x1 = int(m.group(2))
                x2 = int(m.group(3))
                self.veins.append(vein(x1, x2, y, y))
            else:
                print("unknown")

    def solve1(self):
        grid = self.run_waterfall()

        count = 0
        for row in grid:
            for val in row:
                if val == SETTLED or val == FLOWING:
                    count += 1
        return str(count)

    def solve2(self):
        grid = self.run_waterfall()

        count = 0
        for row in grid:
            for val in row:
                if val == SETTLED:
                    count += 1
        return str(count)

    def run_waterfall(self):
        min_x = min(self.veins, key = lambda v: v.x1).x1 - 1
        max_x = max(self.veins, key = lambda v: v.x2).x2 + 2
        min_y = min(self.veins, key = lambda v: v.y1).y1
        max_y = max(self.veins, key = lambda v: v.y2).y2 + 1
        print(min_x, max_x, min_y, max_y)

        grid = [[SAND for x in range(min_x, max_x)] for y in range(min_y, max_y)]
        for v in self.veins:
            for x in range(v.x1, v.x2 + 1):
                for y in range(v.y1, v.y2 + 1):
                    grid[y - min_y][x - min_x] = CLAY

        self.process_well(500 - min_x, 0, grid)
        return grid

    def process_well(self, well_x, well_y, grid):
        max_y = len(grid)
        y = well_y
        while y < max_y and grid[y][well_x] == SAND:
            grid[y][well_x] = FLOWING
            y += 1
        if y == max_y:
            # Running off-grid
            return

        while grid[y][well_x] >= SETTLED and y >= well_y:
            y -= 1
            # Check if we can settle water on top of this row
            left_bound = self.flow(well_x, y, grid, -1)
            right_bound = self.flow(well_x, y, grid, +1)
            if grid[y][left_bound] == CLAY and grid[y][right_bound] == CLAY:
                # Water is settled, bound to the left and right by clay
                for x in range(left_bound + 1, right_bound):
                    grid[y][x] = SETTLED
            else:
                # Water is flowing off at at least one side
                if grid[y][left_bound] == SAND:
                    self.process_well(left_bound, y, grid)
                if grid[y][right_bound] == SAND:
                    self.process_well(right_bound, y, grid)

    def flow(self, x, y, grid, dx):
        x += dx
        while grid[y + 1][x] >= SETTLED and grid[y][x] < SETTLED:
            grid[y][x] = FLOWING
            x += dx
        return x

    def debug(self, grid):
        for row in grid:
            for val in row:
                print(convert(val), end = '')
            print()

day17().test('Sample input', [
    'x=495, y=2..7',
    'y=7, x=495..501',
    'x=501, y=3..7',
    'x=498, y=2..4',
    'x=506, y=1..2',
    'x=498, y=10..13',
    'x=504, y=10..13',
    'y=13, x=498..504'
], '57', '29')

day17().test('Bucket in bucket', [
    'x=495, y=2..10',
    'y=10, x=495..510',
    'x=510, y=3..10',
    'x=501, y=5..7',
    'x=504, y=5..7',
    'y=7, x=501..504'
], '114')

day17().solve()
