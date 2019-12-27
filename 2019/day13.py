import adventofcode
import intcode

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(13)

    def reset(self):
        self.data = []
        # only used in part 2
        self.ball = (0, 0)
        self.paddle = (0, 0)
        self.tiles = dict()

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computer = intcode.computer(list(self.data))

        result = 0
        for _, _, tile_id in zip(*(computer.iterator(),) * 3):
            if tile_id == BLOCK:
                result += 1

        return str(result)

    def solve2(self):
        self.data[0] = 2
        computer = intcode.computer(list(self.data))
        score = 0
        for x, y, tile_id in computer.iterator_triple():
            if x == -1 and y == 0:
                score = tile_id
                break
            self.tiles[(x, y)] = tile_id
            if tile_id == BALL:
                self.ball = (x, y)
            elif tile_id == PADDLE:
                self.paddle = (x, y)

        for x, y, tile_id in computer.iterator_triple(self.provide_input):
            if x == -1 and y == 0:
                score = tile_id
            else:
                self.tiles[(x, y)] = tile_id
                if tile_id == BALL:
                    self.ball = (x, y)
                elif tile_id == PADDLE:
                    self.paddle = (x, y)

        return str(score)
                
    def provide_input(self, computer):
        #self.print_board()
        if self.ball[0] < self.paddle[0]:
            computer.input.append(-1)
        elif self.ball[0] == self.paddle[0]:
            computer.input.append(0)
        else:
            computer.input.append(1)

    def print_board(self):
        x_max = max(self.tiles.keys(), key = lambda p: p[0])[0] + 1
        y_max = max(self.tiles.keys(), key = lambda p: p[1])[1] + 1
        for y in range(y_max):
            for x in range(x_max):
                tile_id = self.tiles[(x, y)]
                if tile_id == EMPTY:
                    print(' ', end = '')
                elif tile_id == WALL:
                    print('#', end = '')
                elif tile_id == BLOCK:
                    print('x', end = '')
                elif tile_id == PADDLE:
                    print('=', end = '')
                elif tile_id == BALL:
                    print('O', end = '')
            print()


r = runner()

r.run()
