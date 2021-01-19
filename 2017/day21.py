import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(21)

    def reset(self):
        self.rules2 = []
        self.rules3 = []

    def input_line(self, line):
        (src, dst) = map(lambda g: g.split('/'), line.split(' => '))
        if len(src) == 2:
            self.rules2.append((src, dst))
        else:
            self.rules3.append((src, dst))

    def solve1(self):
        self.lookup2 = self.transform_rules2()
        self.lookup3 = self.transform_rules3()
        grid = [
            '.#.',
            '..#',
            '###'
        ]
        for n in range(5):
            if len(grid) % 2 == 0:
                grid = self.enhance(grid, self.lookup2, 2)
            else:
                grid = self.enhance(grid, self.lookup3, 3)
        return str(sum(map(lambda row: sum(map(lambda x: 1 if x == '#' else 0, row)), grid)))

    def solve2(self):
        # size 3 -> size 4 -> size 6 -> size 9
        # Size 9 consists of 9 totally independent 3x3 squares, so those can be
        # calculated separately without having to simulate the whole grid
        lookup = dict()
        bitcount = dict()
        for n in range(512):
            grid = self.enhance(self.enhance(self.lookup3[n], self.lookup2, 2), self.lookup2, 2)
            result = []
            for y in range(3):
                for x in range(3):
                    result.append(self.get_id(grid, 3, x * 3, y * 3))
            lookup[n] = result
            bitcount[n] = self.count_bits(n)

        start = self.get_id([
            '.#.',
            '..#',
            '###'
        ], 3)
        squares = [start]
        for n in range(6):
            new_squares = []
            for id in squares:
                new_squares.extend(lookup[id])
            squares = new_squares

        return str(sum(map(lambda x: bitcount[x], squares)))

    def count_bits(self, n):
        bits = 0
        while n:
            if n & 1:
                bits += 1
            n >>= 1
        return bits

    def enhance(self, grid, lookup, block_size):
        result = ['' for y in range((block_size + 1) * len(grid) // block_size)]
        for block_y in range(len(grid) // block_size):
            for block_x in range(len(grid) // block_size):
                id = self.get_id(grid, block_size, block_x * block_size, block_y * block_size)
                for y, row in enumerate(lookup[id]):
                    result[block_y * (block_size + 1) + y] += row
        return result

    def transform_rules2(self):
        lookup = dict()
        for src, dst in self.rules2:
            for n in range(4):
                id = self.get_id(src, 2)
                lookup[id] = dst
                src = self.rotate_image(src)
            # No need to flip: all cases are covered by rotation
        return lookup

    def transform_rules3(self):
        lookup = dict()
        for src, dst in self.rules3:
            for n in range(4):
                id = self.get_id(src, 3)
                lookup[id] = dst
                src = self.rotate_image(src)
            src = self.flip_image(src)
            for n in range(4):
                id = self.get_id(src, 3)
                lookup[id] = dst
                src = self.rotate_image(src)
        return lookup

    def get_id(self, img, size, x = 0, y = 0):
        result = 0
        for dy in range(size):
            for dx in range(size):
                result <<= 1
                if img[y + dy][x + dx] == '#':
                    result |= 1
        return result

    def rotate_image(self, img):
        return [[img[x][y] for x in range(len(img[0])-1, -1, -1)] for y in range(len(img))]

    def flip_image(self, img):
        return [[img[y][x] for x in range(len(img[0])-1, -1, -1)] for y in range(len(img))]

r = runner()
r.run()
