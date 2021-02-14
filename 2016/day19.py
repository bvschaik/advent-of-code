import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(19)

    def reset(self):
        self.elves = 0

    def input_line(self, line):
        self.elves = int(line)

    def solve1(self):
        power_of_two = self.max_power_of_n(2, self.elves)
        rest = self.elves - power_of_two
        return str(1 + rest * 2)

    def solve2(self):
        power_of_three = self.max_power_of_n(3, self.elves)
        higher_power_of_three = power_of_three * 3
        if self.elves < 2 * power_of_three:
            return str(self.elves - power_of_three)
        else:
            return str(higher_power_of_three - 2 * (higher_power_of_three - self.elves))

    def max_power_of_n(self, n, value):
        power = 1
        while power < value:
            power *= n
        return power // n

r = runner()
r.run()
