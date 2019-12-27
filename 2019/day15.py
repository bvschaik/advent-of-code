import adventofcode
import intcode

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

STEP = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    EAST: (1, 0)
}

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST
}

WALL = 0
SPACE = 1
OXYGEN = 2

class repair_droid:
    def __init__(self, program):
        self.computer = intcode.computer(program)

    def move(self, direction):
        self.computer.input.append(direction)
        return self.computer.run_until_output()

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(15)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        droid = repair_droid(list(self.data))
        area_map = dict()
        coord = (0, 0)
        area_map[coord] = SPACE

        _, dist = self.recurse(droid, area_map, coord)

        # self.print_map(area_map)
        return str(dist)

    def recurse(self, droid, area_map, coord, coming_from = 0):
        for d in range(1, 5):
            if d == coming_from:
                continue
            new_coord = (coord[0] + STEP[d][0], coord[1] + STEP[d][1])
            if new_coord in area_map:
                continue
            tile = droid.move(d)
            area_map[new_coord] = tile
            if tile == OXYGEN:
                # print("Found oxygen at", new_coord)
                return (True, 1)
            elif tile == SPACE:
                found, dist = self.recurse(droid, area_map, new_coord, OPPOSITE[d])
                if found:
                    return (True, dist + 1)
                # Move back
                droid.move(OPPOSITE[d])

        return (False, 0)

    def solve2(self):
        droid = repair_droid(list(self.data))
        area_map = dict()
        coord = (0, 0)
        area_map[coord] = SPACE

        oxygen_coord = self.recurse_all(droid, area_map, coord)

        oxygen_map = {oxygen_coord}

        minute = -1
        to_process = {oxygen_coord}
        while to_process:
            minute += 1
            new_to_process = set()
            for coord in to_process:
                # print('providing oxygen to', coord)
                oxygen_map.add(coord)
                for d in range(1, 5):
                    new_coord = (coord[0] + STEP[d][0], coord[1] + STEP[d][1])
                    if new_coord not in oxygen_map and new_coord in area_map and area_map[new_coord] != WALL:
                        new_to_process.add(new_coord)
            to_process = new_to_process

        return minute

    def recurse_all(self, droid, area_map, coord):
        oxygen = None
        for d in range(1, 5):
            new_coord = (coord[0] + STEP[d][0], coord[1] + STEP[d][1])
            if new_coord in area_map:
                continue
            tile = droid.move(d)
            area_map[new_coord] = tile
            if tile != WALL:
                if tile == OXYGEN:
                    oxygen = new_coord
                oxygen = self.recurse_all(droid, area_map, new_coord) or oxygen
                # Move back
                droid.move(OPPOSITE[d])
        return oxygen

    def print_map(self, area_map):
        min_x = min(area_map, key = lambda p: p[0])[0]
        max_x = max(area_map, key = lambda p: p[0])[0] + 1
        min_y = min(area_map, key = lambda p: p[1])[1]
        max_y = max(area_map, key = lambda p: p[1])[1] + 1

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                coord = (x, y)
                if x == 0 and y == 0:
                    print('x', end = '')
                elif coord not in area_map:
                    print('?', end = '')
                else:
                    tile = area_map[coord]
                    if tile == WALL:
                        print('#', end = '')
                    elif tile == OXYGEN:
                        print('O', end = '')
                    elif x == 0 and y == 0:
                        print('x', end = '')
                    else:
                        print('.', end = '')
            print()

r = runner()

r.run()
