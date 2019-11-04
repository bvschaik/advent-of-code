import re
from runner import runner

class claim:
    def __init__(self, line):
        m = re.match(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$", line)
        self.id = int(m.group(1))
        self.left = int(m.group(2))
        self.top = int(m.group(3))
        self.width = int(m.group(4))
        self.height= int(m.group(5))

    def __repr__(self):
        return str.format("claim(id=%d, left=%d, top=%d, width=%d, height=%d)\n" % (self.id, self.left, self.top, self.width, self.height))

class day03(runner):
    def __init__(self):
        self.inputs = []

    def day(self):
        return 3
    
    def input(self, line):
        self.inputs.append(claim(line))

    def solve1(self):
        claims_left = sorted(self.inputs, key = lambda x: x.left * 1000 + x.width)
        rows = dict()
        for claim in claims_left:
            for i in range(claim.height):
                row = claim.top + i
                if row not in rows:
                    rows[row] = []
                rows[row].append(claim)

        overlap_tiles = 0
        for (id, row) in rows.items():
            overlap_tiles += self.count_overlap(id, row)

        return str(overlap_tiles)

    def count_overlap(self, id, claims):
        overlap_tiles = 0
        index_counted = 0
        occupied_to = 0
        for claim in claims:
            c_from = claim.left
            c_to = claim.left + claim.width
            if c_from < occupied_to:
                # We have overlap, count tiles starting from index_counted or c_from, whichever is later
                start = max(index_counted, c_from)
                end = min(occupied_to, c_to)
                if end > start:
                    overlap_tiles += end - start
                    index_counted = end
            occupied_to = max(occupied_to, c_to)
        return overlap_tiles

    def solve2(self):
        pass

day03().test('Sample problem', [
    '#1 @ 1,3: 4x4',
    '#2 @ 3,1: 4x4',
    '#3 @ 5,5: 2x2'
], '4')

day03().solve()
