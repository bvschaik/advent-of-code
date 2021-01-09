import adventofcode

WIDTH = 50
HEIGHT = 6

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(8)

    def reset(self):
        self.commands = []

    def input_line(self, line):
        self.commands.append(line.split(' '))

    def solve1(self):
        grid = [[False] * WIDTH for y in range(HEIGHT)]
        for c in self.commands:
            if c[0] == 'rect':
                (width, height) = map(int, c[1].split('x'))
                for y in range(height):
                    for x in range(width):
                        grid[y][x] = True
            elif c[0] == 'rotate':
                if c[1] == 'row':
                    y = int(c[2][2:])
                    size = int(c[4])
                    new_row = list()
                    for x in range(WIDTH):
                        new_row.append(grid[y][(x - size) % WIDTH])
                    grid[y] = new_row
                elif c[1] == 'column':
                    x = int(c[2][2:])
                    size = int(c[4])
                    new_col = list()
                    for y in range(HEIGHT):
                        new_col.append(grid[(y - size) % HEIGHT][x])
                    for y in range(HEIGHT):
                        grid[y][x] = new_col[y]
        self.grid = grid
        return str(sum(map(sum, grid)))

    def solve2(self):
        for row in self.grid:
            print(''.join(map(lambda x: '#' if x else ' ', row)))
        return 'See above'

r = runner()
r.run()
