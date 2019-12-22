import adventofcode
import intcode
from collections import defaultdict

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

NEXT_LEFT = [LEFT, UP, RIGHT, DOWN]
NEXT_RIGHT = [RIGHT, DOWN, LEFT, UP]

DIRECTION_XY = [(0, -1), (1, 0), (0, 1), (-1, 0)]

TURN_LEFT = 0
TURN_RIGHT = 1

BLACK = 0
WHITE = 1

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(11)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computer = intcode.computer(list(self.data), [BLACK])
        tiles = defaultdict(int)
        position = (0, 0)
        direction = UP
        panels_painted = set()
        for paint, move in zip(*(computer.iterator(),) * 2):
            tiles[position] = paint
            panels_painted.add(position)
            if move == TURN_LEFT:
                direction = NEXT_LEFT[direction]
            elif move == TURN_RIGHT:
                direction = NEXT_RIGHT[direction]
            position = (position[0] + DIRECTION_XY[direction][0], position[1] + DIRECTION_XY[direction][1])
            computer.input.append(tiles[position])

        # self.print_tiles(tiles)
        return len(panels_painted)

    def solve2(self):
        computer = intcode.computer(list(self.data), [WHITE])
        tiles = defaultdict(int)
        position = (0, 0)
        direction = UP
        for paint, move in zip(*(computer.iterator(),) * 2):
            #print(position, paint, move)
            tiles[position] = paint
            if move == TURN_LEFT:
                direction = NEXT_LEFT[direction]
            elif move == TURN_RIGHT:
                direction = NEXT_RIGHT[direction]
            position = (position[0] + DIRECTION_XY[direction][0], position[1] + DIRECTION_XY[direction][1])
            computer.input.append(tiles[position])

        self.print_tiles(tiles)
        return 'see above'

    def print_tiles(self, tiles):
        min_x = min(tiles, key = lambda p: p[0])[0]
        max_x = max(tiles, key = lambda p: p[0])[0] + 1
        min_y = min(tiles, key = lambda p: p[1])[1]
        max_y = max(tiles, key = lambda p: p[1])[1] + 1

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                print(' ' if tiles[(x, y)] == BLACK else '#', end = '')
            print()

r = runner()

r.run()
