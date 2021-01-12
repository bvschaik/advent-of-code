import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(1)

    def reset(self):
        self.input = []

    def input_line(self, line):
        self.input = list(map(int, line))

    def solve1(self):
        total = self.input[0] if self.input[0] == self.input[len(self.input) - 1] else 0
        for i in range(len(self.input) - 1):
            if self.input[i] == self.input[i+1]:
                total += self.input[i]
        return str(total)

    def solve2(self):
        half = len(self.input) // 2
        total = 0
        for i in range(half):
            if self.input[i] == self.input[half + i]:
                total += 2 * self.input[i]
        return str(total)

r = runner()

r.test('Sample', [
    '91212129',
], '9')

r.run()
