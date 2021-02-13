import adventofcode
import re

class disc:
    def __init__(self, disc_id, start, positions):
        # Calculation: (where p = positions)
        # (disc + start + time) % p = 0
        # (disc + start) % p + time % p = {0 or p}
        # -> time % p = p - (disc + start) % p iff (disc + start) % p > 0
        # -> time % p = 0 iff (disc + start) % p = 0
        disc_plus_start = (disc_id + start) % positions
        if disc_plus_start == 0:
            self.target = 0
        else:
            self.target = positions - disc_plus_start
        self.disc_id = disc_id
        self.positions = positions

    def combine_with(self, other_disc):
        max_positions = self.positions * other_disc.positions
        result = -1
        for test_target in range(self.target, max_positions, self.positions):
            if test_target % other_disc.positions == other_disc.target:
                self.target = test_target
                self.positions = max_positions
                break

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(15)

    def reset(self):
        self.discs = []

    def input_line(self, line):
        m = re.match(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).', line)
        self.discs.append(disc(int(m.group(1)), int(m.group(3)), int(m.group(2))))

    def solve1(self):
        result = self.create_unit_disc()
        for d in self.discs:
            result.combine_with(d)
        return str(result.target)

    def solve2(self):
        result = self.create_unit_disc()
        for d in self.discs:
            result.combine_with(d)
        result.combine_with(disc(self.discs[-1].disc_id + 1, 0, 11))
        return str(result.target)

    def create_unit_disc(self):
        return disc(0, 0, 1)

r = runner()
r.run()
