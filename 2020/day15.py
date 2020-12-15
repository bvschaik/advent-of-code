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
        index = dict()
        for i, n in enumerate(self.numbers):
            index[n] = [i]

        last = self.numbers[-1]
        for i in range(len(self.numbers), 2020):
            if last not in index or len(index[last]) == 1:
                last = 0
            else:
                occurrences = index[last]
                last = occurrences[-1] - occurrences[-2]
            if last in index:
                index[last].append(i)
            else:
                index[last] = [i]
        return str(last)

    def solve2(self):
        index = dict()
        # Assumption: no duplicates in initial set
        for i, n in enumerate(self.numbers):
            index[n] = i

        last_index = len(self.numbers) - 1
        last_number = self.numbers[-1]
        for i in range(len(self.numbers), 30000000):
            last_number = index[last_number] - last_index
            if last_number in index:
                last_index = index[last_number]
            else:
                last_index = i
            index[last_number] = i
        return str(last_number)
        # 30000000

r = runner()

r.test('Sample 1', ['0,3,6'], '436')
r.test('Sample 2', ['1,3,2'], '1')
r.test('Sample 3', ['2,1,3'], '10')
r.test('Sample 4', ['1,2,3'], '27')
r.test('Sample 5', ['2,3,1'], '78')
r.test('Sample 6', ['3,2,1'], '438')
r.test('Sample 7', ['3,1,2'], '1836')

r.run()
