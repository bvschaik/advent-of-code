import adventofcode
import math
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(16)

    def reset(self):
        self.input = ''

    def input_line(self, line):
        self.input = list(map(int, line))

    def solve1(self):
        data = self.input
        for _ in range(100):
            data = self.transform(data)
            #print(''.join(map(str, data[-4:])))

        return ''.join(map(str, data[:8]))

    def transform(self, input):
        output = []
        for i in range(len(input)):
            output.append(self.transform_digit(input, i + 1))
        return output

    def transform_digit(self, input, index): # index: 1..len(input)
        max_index = len(input)
        result = 0
        step = index * 4
        for start in range(index - 1, max_index, step):
            # Add ones
            for x in range(start, min(start + index, max_index)):
                result += input[x]
            # Subtract minus ones
            nstart = start + index * 2
            for x in range(nstart, min(nstart + index, max_index)):
                result -= input[x]

        return abs(result) % 10

    def solve2(self):
        data = self.input * 10000
        n = int(''.join(map(str, self.input[:7])))
        assert n >= len(data) // 2

        data = data[n:]
        self.transform100(data)
        
        print(data[:8])
        return ''.join(map(str, data[:8]))

    def transform100(self, data):
        max_index = len(data)
        for _ in range(100):
            for i in range(max_index - 2, -1, -1):
                data[i] = (data[i + 1] + data[i]) % 10

r = runner()

#r.test('Sample', ['80871224585914546619083218645595'], '24176176')

# r.test('Sample 2a', ['03036732577212944063491565474664'], None, '84462026')
# r.test('Sample 2b', ['02935109699940807407585447034323'], None, '78725270')

r.run()
