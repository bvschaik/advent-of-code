import adventofcode
import re

class instruction:
    def __init__(self, command, x_from, y_from, x_to, y_to):
        self.command = command
        self.x_from = x_from
        self.y_from = y_from
        self.x_to = x_to
        self.y_to = y_to

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(6)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        m = re.match(r'(turn on|toggle|turn off) (\d+),(\d+) through (\d+),(\d+)', line)
        self.instructions.append(instruction(m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))))

    def solve1(self):
        grid = [[False] * 1000 for _ in range(1000)]
        for instr in self.instructions:
            for y in range(instr.y_from, instr.y_to + 1):
                for x in range(instr.x_from, instr.x_to + 1):
                    if instr.command == 'turn on':
                        grid[y][x] = True
                    elif instr.command == 'turn off':
                        grid[y][x] = False
                    else:
                        grid[y][x] = not grid[y][x]
        count_on = 0
        for row in grid:
            for bulb in row:
                if bulb:
                    count_on += 1
        return str(count_on)

    def solve2(self):
        grid = [[0] * 1000 for _ in range(1000)]
        for instr in self.instructions:
            for y in range(instr.y_from, instr.y_to + 1):
                for x in range(instr.x_from, instr.x_to + 1):
                    if instr.command == 'turn on':
                        grid[y][x] += 1
                    elif instr.command == 'turn off':
                        grid[y][x] = max(grid[y][x] - 1, 0)
                    else:
                        grid[y][x] += 2
        brightness = 0
        for row in grid:
            for bulb in row:
                brightness += bulb
        return str(brightness)

r = runner()

r.test('Sample 1', ['turn on 0,0 through 999,999'], '1000000')

r.run()
