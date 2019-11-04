import string
from runner import runner

class day05(runner):
    def __init__(self):
        self.input_line = None

    def day(self):
        return 5
    
    def input(self, line):
        self.input_line = line

    def solve1(self):
        return str(self.reduce(self.input_line))

    def solve2(self):
        letters = map(lambda x: (x, x.upper()), string.ascii_lowercase)

        return str(min(map(lambda x: self.reduce(self.input_line.replace(x[0], "").replace(x[1], "")), letters)))

    def reduce(self, polymer):
        replacements = list(map(lambda x: x + x.upper(), string.ascii_lowercase)) + list(map(lambda x: x.upper() + x, string.ascii_lowercase))
        start_len = 1 + len(polymer)
        while start_len > len(polymer):
            start_len = len(polymer)
            for r in replacements:
                polymer = polymer.replace(r, "")
        return len(polymer)


day05().test('Sample problem', ['dabAcCaCBAcCcaDA'], '10')

day05().solve()
