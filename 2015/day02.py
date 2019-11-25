import adventofcode
import re

class box:
    def __init__(self, x, y, z):
        self.sides = [x, y, z]
        self.sides.sort()

    def wrapping_paper_area(self):
        (l, w, h) = self.sides
        return 2*l*w + 2*w*h + 2*h*l + l*w

    def ribbon_length(self):
        (l, w, h) = self.sides
        return 2 * (l + w) + l * w * h

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(2)

    def reset(self):
        self.boxes = []

    def input_line(self, line):
        m = re.match(r'(\d+)x(\d+)x(\d+)', line)
        self.boxes.append(box(int(m.group(1)), int(m.group(2)), int(m.group(3))))

    def solve1(self):
        return str(sum(map(lambda b: b.wrapping_paper_area(), self.boxes)))

    def solve2(self):
        return str(sum(map(lambda b: b.ribbon_length(), self.boxes)))

r = runner()

r.test('Sample 1', ['2x3x4'], '58', '34')
r.test('Sample 2', ['1x1x10'], '43', '14')

r.run()
