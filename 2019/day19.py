import adventofcode
import intcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(19)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        count = 0
        for (start, end) in self.get_beam_boundaries(50):
            count += min(end, 50) - min(start, 50)
        return str(count)

    def solve2(self):
        (x, y) = self.get_santa_in_beam()
        return str(x * 10000 + y)

    def get_beam_boundaries(self, limit = 10000):
        yield((0, 1))
        beam_start = 0
        beam_end = 0
        for y in range(1, limit):
            next_beam_start = -1
            for x in range(beam_start, y * 3):
                if self.is_in_beam(x, y):
                    next_beam_start = x
                    break

            if next_beam_start >= 0:
                next_beam_end = max(beam_end, next_beam_start + 1)
                while self.is_in_beam(next_beam_end, y):
                    next_beam_end += 1
                beam_start = next_beam_start
                beam_end = next_beam_end
            yield (beam_start, beam_end)

    def is_in_beam(self, x, y):
        computer = intcode.computer(self.data, [x, y])
        return computer.run_until_output() == 1

    def get_santa_in_beam(self, santa_size = 100):
        boundaries = []
        y = -santa_size
        for values in self.get_beam_boundaries():
            boundaries.append(values)
            # Juggling with y to make sure we have enough values to be able to index y + santa_size - 1
            y += 1
            if y < santa_size:
                continue
            x_start = boundaries[y + santa_size - 1][0]
            x_end = boundaries[y][1]
            if x_end - x_start >= santa_size:
                return (x_start, y)

r = runner()

r.run()
