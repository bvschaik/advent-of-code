import adventofcode

ADJACENT = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(3)

    def reset(self):
        self.square = 0

    def input_line(self, line):
        self.square = int(line)

    def solve1(self):
        # First find out how big the total square is that contains our square
        size = 1
        while size * size < self.square:
            size += 2
        steps_to_ring = (size - 1) // 2
        ring_middle = size * size - (size - 1) // 2
        steps_on_ring = abs(ring_middle - self.square)
        while steps_on_ring > size // 2:
            ring_middle -= (size - 1)
            steps_on_ring = abs(ring_middle - self.square)
        return str(steps_on_ring + steps_to_ring)

    def solve2(self):
        values = {(0, 0): 1}
        for x, y in self.all_squares():
            value = self.sum_adjacent(x, y, values)
            if value > self.square:
                return str(value)
            else:
                values[(x, y)] = value

    def all_squares(self):
        ring = 1
        while True:
            x = ring
            for y in range(-ring + 1, ring + 1):
                yield (x, y)
            y = ring
            for x in range(ring - 1, -ring - 1, -1):
                yield (x, y)
            x = -ring
            for y in range(ring - 1, -ring - 1, -1):
                yield (x, y)
            y = -ring
            for x in range(-ring + 1, ring + 1):
                yield (x, y)
            ring += 1

    def sum_adjacent(self, x, y, values):
        total = 0
        for dx, dy in ADJACENT:
            a = (x + dx, y + dy)
            if a in values:
                total += values[a]
        return total


r = runner()

r.test('Sample', [
    '1024',
], '31')

r.run()
