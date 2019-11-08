from runner import runner

class day11(runner):
    def __init__(self):
        self.serial = 0

    def day(self):
        return 11

    def input(self, line):
        self.serial = int(line) % 1000

    def solve1(self):
        matrix = [[0] * 300 for _ in range(0, 300)]

        for y in range(300):
            for x in range(300):
                matrix[y][x] = self.get_fuel(x + 1, y + 1)

        # Calculate for for every row: sum of [x x+1 x+2]
        for y in range(300):
            for x in range(298):
                matrix[y][x] += matrix[y][x+1] + matrix[y][x+2]

        # Calculate for every column: sum of [y y+1 y+2]
        for x in range(298):
            for y in range(298):
                matrix[y][x] += matrix[y+1][x] + matrix[y+2][x]

        max_value = 0
        max_coord = None
        for x in range(1, 299):
            for y in range(1, 299):
                if matrix[y][x] > max_value:
                    max_value = matrix[y][x]
                    max_coord = (x + 1, y + 1)
        
        return str.format("%d,%d" % max_coord)

    def solve2(self):
        matrix_1 = [[0] * 300 for _ in range(300)]
        matrix_xn = [[0] * 300 for _ in range(300)] # matrix with sums of horizontal 'bricks' of n x 1
        matrix_yn = [[0] * 300 for _ in range(300)] # matrix with sums of vertical 'bricks' of n x 1
        matrix_nn = [[0] * 300 for _ in range(300)] # matrix with sums of squares n x n
        max_value = 0
        max_coord = None

        for y in range(300):
            for x in range(300):
                value = matrix_nn[y][x] = matrix_xn[y][x] = matrix_yn[y][x] = matrix_1[y][x] = self.get_fuel(x + 1, y + 1)
                if value > max_value:
                    max_value = value
                    max_coord = (x + 1, y + 1, 1)

        # Dynamic programming solution: squares n x n are calculated by the sum of:
        # - square (n-1) x (n-1) at (x, y)
        # - vertical brick of n x 1 starting at (x + offset, y)
        # - horizontal brick of n x 1 starting at (x, y + offset)
        # - single item at (x + offset, y + offset)
        # Time complexity: O(n^3)
        for offset in range(1, 299):
            iters = 300 - offset

            # Calculate bricks
            for y in range(iters):
                for x in range(iters):
                    matrix_xn[y][x] += matrix_1[y][x + offset]
                    matrix_yn[y][x] += matrix_1[y + offset][x]
            # Calculate n x n squares
            for y in range(iters):
                for x in range(iters):
                    value = matrix_nn[y][x] = matrix_nn[y][x] + matrix_xn[y+offset][x] + matrix_yn[y][x+offset] + matrix_1[y+offset][x+offset]
                    if value > max_value:
                        #print("Updating max to %d at %dx%d with size %d" % (value, x+1, y+1, offset + 1))
                        max_value = value
                        max_coord = (x + 1, y + 1, offset + 1)

        return str.format("%d,%d,%d" % max_coord)

    def get_fuel(self, x, y):
        rack = x + 10
        power = (rack * y + self.serial) * rack
        power = int((power % 1000) / 100) - 5 # you end up with a number between -5 and 4
        return power


day11().test('Sample input', ['18'], '33,45', '90,269,16')
#day11().test('Sample input 2', ['42'], '21,61')

day11().solve()
