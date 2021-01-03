import adventofcode
import re

class star_point:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def close_to(self, other):
        return abs(self.a - other.a) + abs(self.b - other.b) + abs(self.c - other.c) + abs(self.d - other.d) <= 3

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(25)

    def reset(self):
        self.stars = []

    def input_line(self, line):
        m = re.match(r'(-?\d+),(-?\d+),(-?\d+),(-?\d+)', line)
        self.stars.append(star_point(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    def solve1(self):
        constellations = []

        for s in self.stars:
            constellations_in_range = []
            for index, c in enumerate(constellations):
                if any(map(lambda s2: s.close_to(s2), c)):
                    constellations_in_range.append(index)
            if not constellations_in_range:
                constellations.append({s})
            elif len(constellations_in_range) == 1:
                constellations[constellations_in_range[0]].add(s)
            else: # Merge multiple constellations
                new_constellation = {s}
                for c_index in reversed(constellations_in_range):
                    new_constellation |= constellations[c_index]
                    del constellations[c_index]
                constellations.append(new_constellation)

        return str(len(constellations))

    def solve2(self):
        pass

r = runner()
r.test('Sample input', [
    '0,0,0,0',
    '3,0,0,0',
    '0,3,0,0',
    '0,0,3,0',
    '0,0,0,3',
    '0,0,0,6',
    '9,0,0,0',
    '12,0,0,0',
], '2')

r.test('Sample input 3', [
    '1,-1,0,1',
    '2,0,-1,0',
    '3,2,-1,0',
    '0,0,3,1',
    '0,0,-1,-1',
    '2,3,-2,0',
    '-2,2,0,0',
    '2,-2,0,-1',
    '1,-1,0,-1',
    '3,2,0,2',
], '3')

r.run()
