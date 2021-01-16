import adventofcode

ADJACENT = [(0, -1), (-1, 0), (1, 0), (0, 1)]

class knot_hash:
    def __init__(self):
        self.numbers = [x for x in range(0, 256)]
        self.position = 0
        self.skip = 0

    def hash_once(self, lengths):
        pos = self.position
        for length in lengths:
            # Reverse substring: using reversed() because moving numbers by
            # ourselves is sloooow in Python (3sec vs 300ms)
            if pos + length < 256:
                self.numbers[pos:pos+length] = reversed(self.numbers[pos:pos+length])
            else:
                part1_length = 256 - pos
                part2_length = length - (256 - pos)
                if part1_length < part2_length:
                    tmp = list(reversed(self.numbers[pos:256]))
                    middle_length = part2_length - part1_length
                    self.numbers[pos:256] = reversed(self.numbers[middle_length:part2_length])
                    self.numbers[0:middle_length] = reversed(self.numbers[0:middle_length])
                    self.numbers[middle_length:part2_length] = tmp
                else:
                    tmp = list(reversed(self.numbers[0:part2_length]))
                    middle_pos = pos + part2_length
                    middle_length = part1_length - part2_length
                    self.numbers[0:part2_length] = reversed(self.numbers[pos:pos+part2_length])
                    self.numbers[middle_pos:256] = reversed(self.numbers[middle_pos:256])
                    self.numbers[pos:pos+part2_length] = tmp
            pos = (pos + length + self.skip) % 256
            self.skip += 1
        self.position = pos
    
    def hash(self, data):
        postfix = [17, 31, 73, 47, 23]
        lengths = list(map(ord, data)) + postfix
        for n in range(64):
            self.hash_once(lengths)
        return self.to_bytes()

    def to_bytes(self):
        values = []
        for block in range(16):
            value = 0
            for n in range(block * 16, block * 16 + 16):
                value = value ^ self.numbers[n]
            values.append(value)
        return values

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(14)

    def reset(self):
        self.key = None

    def input_line(self, line):
        self.key = line

    def solve1(self):
        values = []
        for n in range(128):
            values.append(knot_hash().hash(self.key + '-' + str(n)))
        self.memory = values
        bits = 0
        for row in values:
            for b in row:
                while b:
                    if b & 1 == 1:
                        bits += 1
                    b = b >> 1
        return str(bits)

    def solve2(self):
        bits = set()
        for y, row in enumerate(self.memory):
            for x, b in enumerate(row):
                for dx in range(8):
                    if b & (1 << (7 - dx)):
                        bits.add((x * 8 + dx, y))

        groups = 0
        while bits:
            self.remove_reachable(bits.pop(), bits)
            groups += 1
        return str(groups)

    def remove_reachable(self, root, unvisited):
        queue = [root]
        while queue:
            p = queue.pop()
            for dx, dy in ADJACENT:
                n = (p[0] + dx, p[1] + dy)
                if n in unvisited:
                    unvisited.remove(n)
                    queue.append(n)

r = runner()

r.test('Sample', ['flqrgnkx'], '8108', '1242')

r.run()
