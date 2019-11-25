import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(3)

    def reset(self):
        self.instructions = ''

    def input_line(self, line):
        self.instructions = line

    def solve1(self):
        current = (0, 0)
        houses = {current}
        for c in self.instructions:
            current = self.next_location(current, c)
            houses.add(current)
        return str(len(houses))

    def solve2(self):
        santa = (0, 0)
        robo = (0, 0)
        houses = {santa}
        for i, c in enumerate(self.instructions):
            if i % 2 == 0:
                santa = self.next_location(santa, c)
                houses.add(santa)
            else:
                robo = self.next_location(robo, c)
                houses.add(robo)
        return str(len(houses))

    def next_location(self, current, direction):
        if direction == '^':
            return (current[0], current[1] - 1)
        elif direction == 'v':
            return (current[0], current[1] + 1)
        elif direction == '<':
            return (current[0] - 1, current[1])
        elif direction == '>':
            return (current[0] + 1, current[1])
        raise AssertionError("Invalid direction:", direction)

r = runner()

r.test('Sample 1', ['>'], '2')
r.test('Sample 2', ['^>v<'], '4', '3')
r.test('Sample 3', ['^v^v^v^v^v'], '2', '11')

r.run()
