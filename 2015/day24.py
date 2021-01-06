import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(24)

    def reset(self):
        self.presents = []

    def input_line(self, line):
        self.presents.append(int(line))

    def solve1(self):
        target_weight = sum(self.presents) // 3
        return self.get_quantum(target_weight)

    def solve2(self):
        target_weight = sum(self.presents) // 4
        return self.get_quantum(target_weight)

    def get_quantum(self, target_weight):
        options = {0: (0, 1)}
        min_size = len(self.presents)
        min_quantum = 0
        for p in reversed(self.presents):
            to_replace = dict()
            for weight in options:
                (size, quantum) = options[weight]
                p_weight = weight + p
                p_size = size + 1
                p_quantum = quantum * p
                if p_weight <= target_weight:
                    if p_weight not in options or p_size < options[p_weight][0] or p_quantum < options[p_weight][1]:
                        to_replace[p_weight] = (p_size, p_quantum)
            for r in to_replace:
                options[r] = to_replace[r]
        return str(options[target_weight])

r = runner()

r.test('Sample', [
    '1',
    '2',
    '3',
    '4',
    '5',
    '7',
    '8',
    '9',
    '10',
    '11',
], '99')

r.run()
