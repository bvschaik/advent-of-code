import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(13)

    def reset(self):
        self.guards = []

    def input_line(self, line):
        (depth, size) = line.split(': ')
        self.guards.append((int(depth), int(size), (int(size) - 1) * 2))

    def solve1(self):
        severity = 0
        for depth, size, period in self.guards:
            if depth % period == 0:
                severity += depth * size
        return str(severity)

    def solve2(self):
        delay = 0
        success = False
        while not success:
            delay += 1
            success = True
            for depth, size, period in self.guards:
                if (depth + delay) % period == 0:
                    success = False
                    break
        return str(delay)

r = runner()

r.test('Sample', [
    '0: 3',
    '1: 2',
    '4: 4',
    '6: 4',
], '24', '10')

r.run()
