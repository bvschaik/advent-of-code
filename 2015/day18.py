import adventofcode

ADJACENT = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(18)

    def reset(self):
        self.grid = []

    def input_line(self, line):
        self.grid.append(line)

    def solve1(self):
        max_y = len(self.grid)
        max_x = len(self.grid[0])
        neighbours = [[0] * max_x for y in range(max_y)]
        active = [[self.grid[y][x] == '#' for x in range(max_x)] for y in range(max_y)]
        for ly in range(max_y):
            for lx in range(max_x):
                if active[ly][lx]:
                    self.update_neighbours(neighbours, lx, ly, 1)

        for n in range(100):
            changes = []
            for y in range(max_y):
                for x in range(max_x):
                    if active[y][x]:
                        if neighbours[y][x] != 2 and neighbours[y][x] != 3:
                            active[y][x] = False
                            changes.append((x, y, -1))
                    else:
                        if neighbours[y][x] == 3:
                            active[y][x] = True
                            changes.append((x, y, +1))
            for (lx, ly, delta) in changes:
                self.update_neighbours(neighbours, lx, ly, delta)

        return str(sum(map(lambda row: sum(map(int, row)), active)))

    def solve2(self):
        max_y = len(self.grid)
        max_x = len(self.grid[0])
        neighbours = [[0] * max_x for y in range(max_y)]
        active = [[self.grid[y][x] == '#' for x in range(max_x)] for y in range(max_y)]
        active[0][0] = True
        active[max_y - 1][0] = True
        active[0][max_x - 1] = True
        active[max_y - 1][max_x - 1] = True
        for ly in range(max_y):
            for lx in range(max_x):
                if active[ly][lx]:
                    self.update_neighbours(neighbours, lx, ly, 1)

        for n in range(100):
            changes = []
            for y in range(max_y):
                for x in range(max_x):
                    if active[y][x]:
                        if (x == 0 or x == max_x - 1) and (y == 0 or y == max_y - 1):
                            # Never turn off the corner lights
                            pass
                        elif neighbours[y][x] != 2 and neighbours[y][x] != 3:
                            active[y][x] = False
                            changes.append((x, y, -1))
                    else:
                        if neighbours[y][x] == 3:
                            active[y][x] = True
                            changes.append((x, y, +1))
            for (lx, ly, delta) in changes:
                self.update_neighbours(neighbours, lx, ly, delta)

        return str(sum(map(lambda row: sum(map(int, row)), active)))

    def update_neighbours(self, neighbours, lx, ly, delta):
        max_x = len(neighbours[0])
        max_y = len(neighbours)
        for (dx, dy) in ADJACENT:
            x = lx + dx
            y = ly + dy
            if x >= 0 and x < max_x and y >= 0 and y < max_y:
                neighbours[y][x] += delta


r = runner()
r.run()
