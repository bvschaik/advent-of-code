import re
from runner import runner

class day22(runner):
    def __init__(self):
        self.depth = 0
        self.target = (0, 0)

    def day(self):
        return 22

    def input(self, line):
        if line.startswith("depth: "):
            self.depth = int(line.split(' ')[1])
        else:
            m = re.match(r'target: (\d+),(\d+)', line)
            self.target = (int(m.group(1)), int(m.group(2)))

    def solve1(self):
        (target_x, target_y) = self.target
        risk = 0
        prev_erosion_row = []
        for y in range(target_y + 1):
            geoindex_row = []
            erosion_row = []
            for x in range(target_x + 1):
                if (x == 0 and y == 0) or (x == target_x and y == target_y):
                    geoindex = 0
                elif y == 0:
                    geoindex = x * 16807
                elif x == 0:
                    geoindex = y * 48271
                else:
                    geoindex = erosion_row[-1] * prev_erosion_row[x]
                erosion = (geoindex + self.depth) % 20183
                geoindex_row.append(geoindex)
                erosion_row.append(erosion)
                risk += erosion % 3
            prev_erosion_row = erosion_row
        return str(risk)

day22().test('Sample input', ['depth: 510', 'target: 10,10'], '114')

day22().solve()
