import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(18)

    def reset(self):
        self.input = None

    def input_line(self, line):
        self.input = line

    def solve1(self):
        return str(self.calculate_safe(40))

    def solve2(self):
        return str(self.calculate_safe(400000))

    def calculate_safe(self, times):
        safe_tiles = list(map(lambda c: c == '.', self.input))
        max_tiles = len(safe_tiles)
        total_safe = 0
        for n in range(times):
            total_safe += sum(safe_tiles)
            left = True
            for i in range(max_tiles):
                center = safe_tiles[i]
                safe_tiles[i] = not(left ^ (safe_tiles[i+1] if i + 1 < max_tiles else True))
                left = center
        return total_safe

r = runner()
r.run()
