import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(24)

    def reset(self):
        self.area = []

    def input_line(self, line):
        self.area.append(line)

    def input_layout(self):
        configuration = 0
        for y, line in enumerate(self.area):
            for x, c in enumerate(line):
                if c == '#':
                    configuration |= 1 << (x + 5 * y)
        return configuration

    def solve1(self):
        current = self.input_layout()
        layouts = {current}
        while True:
            current = self.evolve(current)
            if current in layouts:
                return str(current)
            layouts.add(current)

    def evolve(self, layout):
        new = 0
        for i in range(25):
            is_bug = (layout & (1 << i)) > 0
            bugs = self.count_adjacent(layout, i)
            if is_bug and bugs == 1:
                new += 1 << i
            elif not is_bug and (bugs == 1 or bugs == 2):
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
        levels = {0: self.input_layout()}
        for _ in range(200):
            levels = self.evolve_recursive(levels)

        return str(self.count_bugs(levels))

    def evolve_recursive(self, levels):
        new_levels = dict()
        for level, layout in levels.items():
            new_levels[level] = self.evolve_recursive_level(level, layout, levels)

        upper_level = max(levels.keys()) + 1
        upper_level_layout = self.evolve_recursive_level(upper_level, 0, levels)
        if upper_level_layout > 0:
            new_levels[upper_level] = upper_level_layout

        lower_level = min(levels.keys()) - 1
        lower_level_layout = self.evolve_recursive_level(lower_level, 0, levels)
        if lower_level_layout > 0:
            new_levels[lower_level] = lower_level_layout

        return new_levels

    def evolve_recursive_level(self, level, layout, levels):
        new_layout = 0
        layout_above = levels[level + 1] if level + 1 in levels else 0
        layout_below = levels[level - 1] if level - 1 in levels else 0
        for i in range(25):
            if i != 12:
                is_bug = (layout & (1 << i)) > 0
                bugs = self.count_adjacent_recursive(layout, i, layout_above, layout_below)
                if is_bug and bugs == 1:
                    new_layout += 1 << i
                elif not is_bug and (bugs == 1 or bugs == 2):
                    new_layout += 1 << i
        return new_layout

    def count_adjacent_recursive(self, layout, i, layout_above, layout_below):
        bugs = 0
        # Above
        if i // 5 == 0: # top row
            if layout_above & (1 << 7) > 0:
                bugs += 1
        elif i == 17: # above is center: take bottom row of below level
            for x in range(20, 25):
                if layout_below & (1 << x) > 0:
                    bugs += 1
        elif layout & (1 << (i - 5)) > 0:
            bugs += 1

        # Below
        if i // 5 == 4: # bottom row
            if layout_above & (1 << 17) > 0:
                bugs += 1
        elif i == 7: # below is center: take top row of below level
            for x in range(0, 5):
                if layout_below & (1 << x) > 0:
                    bugs += 1
        elif layout & (1 << (i + 5)) > 0:
            bugs += 1

        # To the left
        if i % 5 == 0: # left column
            if layout_above & (1 << 11) > 0:
                bugs += 1
        elif i == 13: # to left is center: take right row of below level
            for x in range(4, 25, 5):
                if layout_below & (1 << x) > 0:
                    bugs += 1
        elif layout & (1 << (i - 1)) > 0:
            bugs += 1

        # To the right
        if i % 5 == 4: # right column
            if layout_above & (1 << 13) > 0:
                bugs += 1
        elif i == 11: # to rigth is center: take left row of below level
            for x in range(0, 25, 5):
                if layout_below & (1 << x) > 0:
                    bugs += 1
        elif layout & (1 << (i + 1)) > 0:
            bugs += 1

        return bugs

    def count_bugs(self, levels):
        bugs = 0
        for layout in levels.values():
            bugs += self.count_bugs_at_level(layout)
        return bugs

    def count_bugs_at_level(self, layout):
        bugs = 0
        while layout > 0:
            if layout & 1:
                bugs += 1
            layout >>= 1
        return bugs

r = runner()

# r.test('Sample', [
#     '....#',
#     '#..#.',
#     '#..##',
#     '..#..',
#     '#....',
# ], '2129920', '99')

r.run()
