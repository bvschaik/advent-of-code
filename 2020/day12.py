import adventofcode

EAST_DIR = (1, 0)
SOUTH_DIR = (0, 1)
WEST_DIR = (-1, 0)
NORTH_DIR = (0, -1)

EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3

DIRECTIONS = [EAST_DIR, SOUTH_DIR, WEST_DIR, NORTH_DIR]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(12)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        self.instructions.append((line[0], int(line[1:])))

    def solve1(self):
        direction = EAST
        x = 0
        y = 0
        for (action, value) in self.instructions:
            if action == 'R':
                direction = (direction + value // 90) % 4
            elif action == 'L':
                direction = (direction - value // 90) % 4
            else:
                if action == 'F':
                    move_dir = DIRECTIONS[direction]
                elif action == 'N':
                    move_dir = NORTH_DIR
                elif action == 'S':
                    move_dir = SOUTH_DIR
                elif action == 'E':
                    move_dir = EAST_DIR
                elif action == 'W':
                    move_dir = WEST_DIR
                x += value * move_dir[0]
                y += value * move_dir[1]
        return str(abs(x) + abs(y))

    def solve2(self):
        x = 0
        y = 0
        wx = 10
        wy = -1
        for (action, value) in self.instructions:
            if action == 'R' or action == 'L':
                steps = value // 90
                if action == 'L':
                    steps = (-steps) % 4
                for n in range(steps):
                    tmp = wx
                    wx = -wy
                    wy = tmp
            elif action == 'F':
                x += value * wx
                y += value * wy
            else:
                if action == 'N':
                    move_dir = NORTH_DIR
                elif action == 'S':
                    move_dir = SOUTH_DIR
                elif action == 'E':
                    move_dir = EAST_DIR
                elif action == 'W':
                    move_dir = WEST_DIR
                wx += value * move_dir[0]
                wy += value * move_dir[1]
        return str(abs(x) + abs(y))

r = runner()

r.test('Sample 1', [
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
], '25', '286')

r.run()
