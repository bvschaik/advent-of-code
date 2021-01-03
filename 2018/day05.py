import adventofcode
import string

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(5)

    def reset(self):
        self.input = None

    def input_line(self, line):
        self.input = line

    def solve1(self):
        return str(len(self.reduce(self.input)))

    def solve2(self):
        polymer = "".join(self.reduce(self.input))

        letters = map(lambda x: (x, x.upper()), string.ascii_lowercase)
        return str(min(map(lambda x: len(self.reduce(polymer.replace(x[0], "").replace(x[1], ""))), letters)))

    def reduce(self, polymer):
        stack = list()
        for letter in polymer:
            if stack and stack[-1] == letter:
                stack.pop()
            else:
                stack.append(letter.swapcase())

        return stack

r = runner()
r.test('Sample problem', ['dabAcCaCBAcCcaDA'], '10', '4')

r.run()
