import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(5)

    def reset(self):
        self.jumps = []

    def input_line(self, line):
        self.jumps.append(int(line))

    def solve1(self):
        jumps = list(self.jumps)
        index = 0
        steps = 0
        max_index = len(jumps)
        while index >= 0 and index < max_index:
            steps += 1
            jumps[index] += 1
            index += jumps[index] - 1
        return str(steps)

    def solve2(self):
        jumps = list(self.jumps)
        index = 0
        steps = 0
        max_index = len(jumps)
        while index < max_index:
            steps += 1
            jump = jumps[index]
            if jump >= 3:
                jumps[index] -= 1
            else:
                jumps[index] += 1
            index += jump
        return str(steps)

r = runner()

r.test('Sample', [
    '0',
    '3',
    '0',
    '1',
    '-3',
], '5', '10')

r.run()
