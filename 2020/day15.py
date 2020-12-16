import adventofcode
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(15)

    def reset(self):
        self.numbers = []

    def input_line(self, line):
        self.numbers = list(map(int, line.split(',')))

    def solve1(self):
        return str(self.get_nth_number(2020))

    def solve2(self):
        return str(self.get_nth_number(30000000))

    def get_nth_number(self, max_n):
        index = [-1] * max_n
        # Assumption: no duplicates in initial set
        for i, n in enumerate(self.numbers):
            index[n] = i

        last_index = len(self.numbers) - 1
        last_number = self.numbers[-1]
        for i in range(len(self.numbers), max_n):
            last_number = index[last_number] - last_index
            if index[last_number] >= 0:
                last_index = index[last_number]
            else:
                last_index = i
            index[last_number] = i
        return last_number

r = runner()

r.test('Sample 1', ['0,3,6'], '436')
r.test('Sample 2', ['1,3,2'], '1')
r.test('Sample 3', ['2,1,3'], '10')
r.test('Sample 4', ['1,2,3'], '27')
r.test('Sample 5', ['2,3,1'], '78')
r.test('Sample 6', ['3,2,1'], '438')
r.test('Sample 7', ['3,1,2'], '1836')

r.run()
