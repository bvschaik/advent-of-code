import adventofcode

def fuel_recursive(amount):
    fuel = amount // 3 - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + fuel_recursive(fuel)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(1)
        self.reset()

    def reset(self):
        self.masses = []

    def input_line(self, line):
        self.masses.append(int(line))

    def solve1(self):
        return str(sum(map(lambda x: x // 3 - 2, self.masses)))

    def solve2(self):
        return str(sum(map(fuel_recursive, self.masses)))

r = runner()

r.test('Sample', ['100756'], '33583', '50346')

r.run()
