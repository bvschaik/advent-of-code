import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(25)

    def reset(self):
        self.input = []

    def input_line(self, line):
        self.input.append(int(line))

    def solve1(self):
        loop1 = self.find_loop_size(self.input[0])
        return str(self.transform(self.input[1], loop1))

    def find_loop_size(self, key):
        n = 0
        value = 1
        subject = 7
        while value != key:
            n += 1
            value = (value * subject) % 20201227
        return n

    def transform(self, subject, loops):
        value = 1
        for n in range(loops):
            value = (value * subject) % 20201227
        return value

    def solve2(self):
        pass

r = runner()

r.test('Sample 1', [
    '5764801',
    '17807724',
], '14897079')

r.run()
