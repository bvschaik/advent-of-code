import adventofcode
from collections import defaultdict

SIZE = 10

TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3

                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
MONSTER = [
    (18, 0),
    (0, 1),
    (5, 1),
    (6, 1),
    (11, 1),
    (12, 1),
    (17, 1),
    (18, 1),
    (19, 1),
    (1, 2),
    (4, 2),
    (7, 2),
    (10, 2),
    (13, 2),
    (16, 2)
]
MONSTER_WIDTH = 20
MONSTER_HEIGHT = 3

class image:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.edges = [
            self.to_lowest_number(self.data[0]),
            self.to_lowest_number(self.data[SIZE-1]),
            self.to_lowest_number(map(lambda x: x[0], self.data)),
            self.to_lowest_number(map(lambda x: x[SIZE-1], self.data))
        ]
        self.used = False

    def opposite_edge(self, edge):
        if edge == self.edges[TOP]:
            return self.edges[BOTTOM]
        if edge == self.edges[BOTTOM]:
            return self.edges[TOP]
        if edge == self.edges[LEFT]:
            return self.edges[RIGHT]
        if edge == self.edges[RIGHT]:
            return self.edges[LEFT]

    def to_lowest_number(self, edge):
        n = 0
        rn = 0
        for i, c in enumerate(edge):
            if c == '#':
                rn |= 1 << i
                n |= 1 << (SIZE - 1 - i)
        return min(n, rn)

    def get_data(self, top_edge, left_edge):
        range_up = range(1, SIZE-1, 1)
        range_down = range(SIZE-2, 0, -1)
        if top_edge == self.edges[TOP]:
            if left_edge == self.edges[LEFT]:
                # return as-is
                return [[self.data[y][x] for x in range_up] for y in range_up]
            else:
                # return flipped left <--> right
                return [[self.data[y][x] for x in range_down] for y in range_up]
        elif top_edge == self.edges[BOTTOM]:
            if left_edge == self.edges[LEFT]:
                # return upside down
                return [[self.data[y][x] for x in range_up] for y in range_down]
            else:
                # return rotated 180 degrees
                return [[self.data[y][x] for x in range_down] for y in range_down]
        elif top_edge == self.edges[LEFT]:
            if left_edge == self.edges[TOP]:
                # mirror over the diagonal
                return [[self.data[x][y] for x in range_up] for y in range_up]
            else:
                # rotate 90 degrees clockwise
                return [[self.data[x][y] for x in range_down] for y in range_up]
        elif top_edge == self.edges[RIGHT]:
            if left_edge == self.edges[TOP]:
                return [[self.data[x][y] for x in range_up] for y in range_down]
            else:
                return [[self.data[x][y] for x in range_down] for y in range_down]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(20)

    def reset(self):
        self.images = dict()
        self.tmp_id = 0
        self.tmp_data = []

    def input_line(self, line):
        if not line:
            self.images[self.tmp_id] = image(self.tmp_id, self.tmp_data)
            self.tmp_id = 0
            self.tmp_data = []
        elif line.startswith('Tile '):
            self.tmp_id = int(line[5:].strip(':'))
        else:
            self.tmp_data.append(line)

    def solve1(self):
        self.edges = defaultdict(list)
        for img in self.images.values():
            for e in img.edges:
                self.edges[e].append(img.id)

        edge_tiles = defaultdict(int)
        for ids in self.edges.values():
            if len(ids) == 1:
                edge_tiles[ids[0]] += 1

        self.corner_tiles = []
        mult = 1
        for id in edge_tiles:
            if edge_tiles[id] == 2:
                self.corner_tiles.append(id)
                mult *= id
        return str(mult)

    def solve2(self):
        img = self.construct_image()
        # self.print_image(img)
        return self.find_monsters(img)

    def rotate_image(self, img):
        return [[img[x][y] for x in range(len(img[0])-1, -1, -1)] for y in range(len(img))]

    def flip_image(self, img):
        return [[img[y][x] for x in range(len(img[0])-1, -1, -1)] for y in range(len(img))]

    def construct_image(self):
        full_data = [[] for y in range(8)]
        top_row_values = []

        # Start at the tile in the first corner
        tile = self.images[self.corner_tiles[0]]
        tile.used = True
        left_value = self.tile_edge(tile)
        top_value = self.tile_edge(tile, left_value)
        top_row_values.append(tile.opposite_edge(top_value))
        self.append_tile(full_data, 0, tile.get_data(top_value, left_value))
        left_value = tile.opposite_edge(left_value)
        # Find first row
        while True:
            tile = self.find_adjacent_tile(left_value)
            if not tile:
                break
            tile.used = True
            top_value = self.tile_edge(tile, tile.opposite_edge(left_value))
            self.append_tile(full_data, 0, tile.get_data(top_value, left_value))
            left_value = tile.opposite_edge(left_value)
            top_row_values.append(tile.opposite_edge(top_value))

        # Find subsequent rows
        y = 8
        while self.find_adjacent_tile(top_row_values[0]):
            full_data.extend([[] for y in range(8)])
            for x in range(len(top_row_values)):
                top_value = top_row_values[x]
                tile = self.find_adjacent_tile(top_value)
                tile.used = True
                if x == 0:
                    left_value = self.tile_edge(tile, tile.opposite_edge(top_value))
                self.append_tile(full_data, y, tile.get_data(top_value, left_value))
                left_value = tile.opposite_edge(left_value)
                top_row_values[x] = tile.opposite_edge(top_value)
            y += 8
        return full_data

    def print_image(self, data):
        for line in data:
            for c in line:
                print(c, end = '')
            print()

    def find_adjacent_tile(self, value):
        for id in self.edges[value]:
            if not self.images[id].used:
                return self.images[id]

    def tile_edge(self, tile, but_not = -1):
        for e in tile.edges:
            if len(self.edges[e]) == 1:
                if e != but_not:
                    return e

    def append_tile(self, full_data, y_offset, tile_data):
        for y, row in enumerate(tile_data):
            full_data[y_offset + y].extend(row)

    def find_monsters(self, img):
        for flip in range(2):
            for r in range(4):
                monsters = self.find_all_monsters(img)
                if monsters:
                    return self.calculate_roughness(img, monsters)
                img = self.rotate_image(img)
            img = self.flip_image(img)

    def find_all_monsters(self, img):
        monsters = []
        for y in range(len(img) - MONSTER_HEIGHT):
            for x in range(len(img[0]) - MONSTER_WIDTH):
                is_monster = True
                for (dx, dy) in MONSTER:
                    if img[y + dy][x + dx] != '#':
                        is_monster = False
                        break
                if is_monster:
                    monsters.append((x, y))
        return monsters

    def calculate_roughness(self, img, monsters):
        black_tiles = set()
        num_black = 0
        for y, line in enumerate(img):
            for x, c in enumerate(img[y]):
                if c == '#':
                    num_black += 1
                    black_tiles.add((x, y))

        return num_black - len(monsters) * len(MONSTER)

r = runner()

r.run()
