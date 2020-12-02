import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(1)

    def reset(self):
        self.numbers = set()

    def input_line(self, line):
        self.numbers.add(int(line))

    def solve1(self):
        for n in self.numbers:
            remainder = 2020 - n
            if remainder in self.numbers:
                return str(n * remainder)
        return None

    def solve2(self):
        for n in self.numbers:
            for m in self.numbers:
                remainder = 2020 - n - m
                if remainder in self.numbers:
                    return str(n * m * remainder)
        return None

r = runner()

r.test('Sample', [
    '1721',
    '979',
    '366',
    '299',
    '675',
    '1456',
], '514579')

r.run()
