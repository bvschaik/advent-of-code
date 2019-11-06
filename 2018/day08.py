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

    def sum_meta(self, index):
        num_children = self.bytes[index]
        num_meta = self.bytes[index + 1]
        index += 2
        meta_sum = 0
        for _ in range(num_children):
            (child_sum, index) = self.sum_meta(index)
            meta_sum += child_sum
        for m in range(num_meta):
            meta_sum += self.bytes[index + m]
        return (meta_sum, index + num_meta)

    def solve2(self):
        (value, _) = self.calculate_value(0)
        return str(value)

    def calculate_value(self, index):
        num_children = self.bytes[index]
        num_meta = self.bytes[index + 1]
        index += 2
        if num_children == 0:
            value = sum([self.bytes[index + m] for m in range(num_meta)])
            return (value, index + num_meta)
        else:
            child_values = [0] * num_children
            for c in range(num_children):
                (child_values[c], index) = self.calculate_value(index)
            parent_value = 0
            for m in range(num_meta):
                child = self.bytes[index + m] - 1
                if child >= 0 and child < num_children:
                    parent_value += child_values[child]
            return (parent_value, index + num_meta)

day08().test('Sample input', ['2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'], '138', '66')

day08().solve()
