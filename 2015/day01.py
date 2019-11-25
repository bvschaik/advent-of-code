import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(1)
        self.floors = ''

    def input_line(self, line):
        self.floors = line

    def solve1(self):
        up = self.floors.count('(')
        down = len(self.floors) - up
        return str(up - down)

    def solve2(self):
        floor = 0
        for index, c in enumerate(self.floors):
            if c == '(':
                floor += 1
            else:
                floor -= 1
            if floor == -1:
                return str(index + 1)

r = runner()

r.test('Sample', ['(()(()('], '3')

r.run()
