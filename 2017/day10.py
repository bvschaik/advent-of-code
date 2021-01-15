import adventofcode

class knot_hash:
    def __init__(self):
        self.numbers = [x for x in range(0, 256)]
        self.position = 0
        self.skip = 0

    def hash_once(self, lengths):
        for length in lengths:
            # Reverse substring
            for n in range(length // 2):
                p1 = (self.position + n) % 256
                p2 = (self.position + length - 1 - n) % 256
                tmp = self.numbers[p1]
                self.numbers[p1] = self.numbers[p2]
                self.numbers[p2] = tmp
            self.position = (self.position + length + self.skip) % 256
            self.skip += 1
    
    def hash(self, data):
        postfix = [17, 31, 73, 47, 23]
        lengths = list(map(ord, data)) + postfix
        for n in range(64):
            self.hash_once(lengths)
        return self.to_hex_string()

    def to_hex_string(self):
        hex_values = []
        for block in range(16):
            value = 0
            for n in range(block * 16, block * 16 + 16):
                value = value ^ self.numbers[n]
            hex_values.append(value)
        hex_chars = '0123456789abcdef'
        hex_string = ''
        for v in hex_values:
            hex_string += hex_chars[v >> 4]
            hex_string += hex_chars[v & 15]
        return hex_string

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(10)

    def reset(self):
        self.lengths = []

    def input_line(self, line):
        self.string = line
        self.lengths = list(map(int, line.split(',')))

    def solve1(self):
        knot = knot_hash()
        knot.hash_once(self.lengths)
        return str(knot.numbers[0] * knot.numbers[1])

    def solve2(self):
        knot = knot_hash()
        return knot.hash(self.string)

r = runner()
r.run()
