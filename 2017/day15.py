import adventofcode
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(15)

    def reset(self):
        self.generators = []

    def input_line(self, line):
        value = int(line.split(' ')[-1])
        self.generators.append(value)

    def solve1(self):
        score = 0
        (a, b) = self.generators
        for n in range(100000):
            a = (a * 16807) % 0x7fffffff
            b = (b * 48271) % 0x7fffffff
            if (a & 0xffff) == (b & 0xffff):
                score += 1
        return str(score)

    def solve2(self):
        score = 0
        (a, b) = self.generators
        for n in range(5000000):
            a = (a * 16807) % 0x7fffffff
            while a & 0x3:
                a = (a * 16807) % 0x7fffffff
            b = (b * 48271) % 0x7fffffff
            while b & 0x7:
                b = (b * 48271) % 0x7fffffff
            if (a & 0xffff) == (b & 0xffff):
                score += 1
        return str(score)

r = runner()
r.run()
