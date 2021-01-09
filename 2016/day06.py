import adventofcode
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(6)

    def reset(self):
        self.inputs = []

    def input_line(self, line):
        self.inputs.append(line)

    def solve1(self):
        message = ''
        for n in range(len(self.inputs[0])):
            letters = defaultdict(int)
            for m in self.inputs:
                letters[m[n]] += 1
            max_key = max(letters.items(), key = lambda x: (x[1]))
            message += max_key[0]
        return message

    def solve2(self):
        message = ''
        for n in range(len(self.inputs[0])):
            letters = defaultdict(int)
            for m in self.inputs:
                letters[m[n]] += 1
            min_key = min(letters.items(), key = lambda x: (x[1]))
            message += min_key[0]
        return message

r = runner()
r.run()
