import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(17)

    def reset(self):
        self.step = 0

    def input_line(self, line):
        self.step = int(line)

    def solve1(self):
        buffer = [0]
        cur = 0
        step = self.step
        for n in range(1, 2018):
            cur = ((cur + step) % n) + 1
            buffer.insert(cur, n)
        return str(buffer[cur + 1])

    def solve2(self):
        cur = 0
        step = self.step + 1
        after_zero = 0
        n = 1
        while n <= 50000000:
            if cur + step >= n:
                cur = (cur + step) % n
                n += 1
            else:
                factor = (n - cur) // step
                cur += factor * step
                n += factor
            if cur == 0:
                after_zero = n - 1
        return str(after_zero)

r = runner()

r.test('Sample', [
    '3',
], '638')

r.run()
