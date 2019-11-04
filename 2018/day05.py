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
        return str(len(self.reduce(self.input_line)))

    def solve2(self):
        polymer = "".join(self.reduce(self.input_line))

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


day05().test('Sample problem', ['dabAcCaCBAcCcaDA'], '10', '4')

day05().solve()
