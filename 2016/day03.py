import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(3)

    def reset(self):
        self.triangles = []

    def input_line(self, line):
        self.triangles.append((
            int(line[0:5].strip()),
            int(line[5:10].strip()),
            int(line[10:15].strip())
        ))

    def solve1(self):
        possible = 0
        for t1, t2, t3 in self.triangles:
            if self.is_possible(t1, t2, t3):
                possible += 1
        return str(possible)

    def solve2(self):
        possible = 0
        for n in range(0, len(self.triangles), 3):
            for p in range(3):
                if self.is_possible(self.triangles[n][p], self.triangles[n+1][p], self.triangles[n+2][p]):
                    possible += 1
        return str(possible)

    def is_possible(self, t1, t2, t3):
        return t1 + t2 > t3 and t1 + t3 > t2 and t2 + t3 > t1

r = runner()
r.run()
