import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(5)

    def reset(self):
        self.passes = []

    def input_line(self, line):
        self.passes.append(line)

    def solve1(self):
        return str(max(map(lambda s: self.to_binary(s), self.passes)))

    def solve2(self):
        all_seats = set(range(0, 1023))
        filled_seats = set(map(lambda s: self.to_binary(s), self.passes))
        available_seats = all_seats - filled_seats
        for seat in all_seats - filled_seats:
            if (seat + 1) in filled_seats and (seat - 1) in filled_seats:
                return str(seat)
        return None

    def to_binary(self, value):
        number = 0
        for c in value:
            number *= 2
            if c == 'B' or c == 'R':
                number += 1
        return number

r = runner()

r.test('Sample 1', [
    'FBFBBFFRLR',
], '357')

r.run()
