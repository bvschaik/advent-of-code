import adventofcode
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(16)

    def reset(self):
        self.initial = None

    def input_line(self, line):
        self.initial = line

    def solve1(self):
        return self.solve_naive(272)

    def solve2(self):
        return self.solve_naive(35651584)

    def solve_naive(self, size):
        values = list(map(int, self.initial))
        while len(values) < size:
            values = self.expand(values)
        values = values[0:size]
        while len(values) % 2 == 0:
            values = self.contract(values)
        return ''.join(map(str, values))

    def expand(self, values):
        result = list(values)
        result.append(0)
        result.extend(map(lambda x: 1 - x, reversed(values)))
        return result

    def contract(self, values):
        result = []
        for i in range(0, (len(values) // 2) * 2, 2):
            result.append(1 if values[i] == values[i+1] else 0)
        return result

    # Notes, if I ever revisit this problem:
    # - The stream consists of ajbjajbjajbjajbj... where j is a joiner value and a, b are as defined in the problem
    # - Joiner values are calculated using the expansion of an empty stream: 0, 001, 0010011, ...
    # - The even indexed values of the joiner stream are 0, 1, 0, 1, 0, 1, ...
    # - Every iteration, only 4 'words' are used in total

r = runner()
r.run()
