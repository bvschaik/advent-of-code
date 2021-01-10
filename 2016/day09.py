import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(9)

    def reset(self):
        self.data = ''

    def input_line(self, line):
        self.data = line

    def solve1(self):
        size = 0
        i = 0
        while i < len(self.data):
            if self.data[i] == '(':
                close = i + self.data[i:].find(')')
                (length, times) = map(int, self.data[i+1:close].split('x'))
                size += length * times
                i = close + length + 1
            else:
                size += 1
                i += 1
        return str(size)

    def solve2(self):
        return str(self.decompressed_size(self.data))

    def decompressed_size(self, data):
        size = 0
        i = 0
        while i < len(data):
            if data[i] == '(':
                close = i + data[i:].find(')')
                (length, times) = map(int, data[i+1:close].split('x'))
                i = close + 1
                subpart = data[i:i+length]
                size += times * self.decompressed_size(subpart)
                i += length
            else:
                size += 1
                i += 1
        return size

r = runner()
r.run()
