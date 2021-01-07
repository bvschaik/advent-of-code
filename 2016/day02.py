import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(2)

    def reset(self):
        self.lines = []

    def input_line(self, line):
        self.lines.append(line)

    def solve1(self):
        keys = {
            (0, 0): '1',
            (1, 0): '2',
            (2, 0): '3',
            (0, 1): '4',
            (1, 1): '5',
            (2, 1): '6',
            (0, 2): '7',
            (1, 2): '8',
            (2, 2): '9'
        }
        return self.find_code(keys, (1, 1))

    def solve2(self):
        keys = {
            (2, 0): '1',
            (1, 1): '2',
            (2, 1): '3',
            (3, 1): '4',
            (0, 2): '5',
            (1, 2): '6',
            (2, 2): '7',
            (3, 2): '8',
            (4, 2): '9',
            (1, 3): 'A',
            (2, 3): 'B',
            (3, 3): 'C',
            (2, 4): 'D',
        }
        return self.find_code(keys, (0, 2))

    def find_code(self, keys, start):
        position = start
        code = []
        for line in self.lines:
            for c in line:
                if c == 'U':
                    new_pos = (position[0], position[1] - 1)
                elif c == 'D':
                    new_pos = (position[0], position[1] + 1)
                elif c == 'L':
                    new_pos = (position[0] - 1, position[1])
                elif c == 'R':
                    new_pos = (position[0] + 1, position[1])
                else:
                    print('unknown char', c)
                if new_pos in keys:
                    position = new_pos
            code.append(keys[position])
        return ''.join(code)

r = runner()
r.run()
