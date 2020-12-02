import adventofcode
import re

class policy:
    def __init__(self, first, second, letter, password):
        self.first = first
        self.second = second
        self.letter = letter
        self.password = password

    def matches_occurrence(self):
        num_letters = self.password.count(self.letter)
        return num_letters >= self.first and num_letters <= self.second

    def matches_position(self):
        letter1 = self.password[self.first - 1]
        letter2 = self.password[self.second - 1]
        return (letter1 == self.letter) ^ (letter2 == self.letter)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(2)

    def reset(self):
        self.lines = []

    def input_line(self, line):
        m = re.match(r'(\d+)-(\d+) ([a-z]): ([a-z]+)', line)
        self.lines.append(policy(int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)))

    def solve1(self):
        return str(sum(map(lambda p: p.matches_occurrence(), self.lines)))

    def solve2(self):
        return str(sum(map(lambda p: p.matches_position(), self.lines)))

r = runner()

r.test('Sample 1', [
    '1-3 a: abcde',
    '1-3 b: cdefg',
    '2-9 c: ccccccccc',
], '2', '1')

r.run()
