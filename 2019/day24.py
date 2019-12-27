import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(24)

    def reset(self):
        self.area = []

    def input_line(self, line):
        self.area.append(line)

    def solve1(self):
        configuration = 0
        for y, line in enumerate(self.area):
            for x, c in enumerate(line):
                if c == '#':
                    configuration |= 1 << (x + 5 * y)

        layouts = {configuration}
        current = configuration
        while True:
            current = self.evolve(current)
            if current in layouts:
                return str(current)
            layouts.add(current)

    def evolve(self, layout):
        new = 0
        bugs = set()
        for i in range(25):
            is_bug = (layout & (1 << i)) > 0
            bugs = self.count_adjacent(layout, i)
            if is_bug == 1 and bugs == 1:
                # print('prolong bug at', i % 5, i // 5, bugs)
                new += 1 << i
            elif is_bug == 0 and (bugs == 1 or bugs == 2):
                # print('birth bug at', i % 5, i // 5)
                new += 1 << i
        return new

    def count_adjacent(self, layout, i):
        bugs = 0
        if i % 5 > 0 and (layout & (1 << i - 1)) > 0:
            bugs += 1
        if i % 5 < 4 and (layout & (1 << i + 1)) > 0:
            bugs += 1
        if i // 5 > 0 and (layout & (1 << i - 5)) > 0:
            bugs += 1
        if i // 5 < 4 and (layout & (1 << i + 5)) > 0:
            bugs += 1
        return bugs

    def print_layout(self, layout):
        print()
        for y in range(5):
            for x in range(5):
                if layout & (1 << 5 * y + x) != 0:
                    print('#', end = '')
                else:
                    print('.', end = '')
            print()

    def solve2(self):
        pass

r = runner()

r.test('Sample', [
    '....#',
    '#..#.',
    '#..##',
    '..#..',
    '#....',
], '2129920')

r.run()
