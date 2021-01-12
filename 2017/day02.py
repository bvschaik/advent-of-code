import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(2)

    def reset(self):
        self.rows = []

    def input_line(self, line):
        self.rows.append(list(map(int, line.split())))

    def solve1(self):
        total = 0
        for row in self.rows:
            total += max(row) - min(row)
        return str(total)

    def solve2(self):
        total = 0
        for row in self.rows:
            for i in range(len(row)):
                x = row[i]
                for j in range(i + 1, len(row)):
                    y = row[j]
                    if x % y == 0:
                        total += x // y
                    elif y % x == 0:
                        total += y // x
        return str(total)

r = runner()
r.run()
