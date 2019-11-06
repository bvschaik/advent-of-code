from runner import runner

class day08(runner):
    def __init__(self):
        self.bytes = []

    def day(self):
        return 8
    
    def input(self, line):
        self.bytes = [int(x) for x in line.split(" ")]

    def solve1(self):
        (sum_of_meta, _) = self.sum_meta(0)
        return str(sum_of_meta)

    def sum_meta(self, index, level = 0):
        num_children = self.bytes[index]
        num_meta = self.bytes[index + 1]
        index += 2
        meta_sum = 0
        for _ in range(num_children):
            (child_sum, index) = self.sum_meta(index, level + 1)
            meta_sum += child_sum
        for m in range(num_meta):
            meta_sum += self.bytes[index + m]
        index += num_meta
        return (meta_sum, index)

    def solve2(self):
        pass

day08().test('Sample input', ['2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'], '138')

day08().solve()
