import adventofcode
import re

class policy:
    def __init__(self, first, second, letter, password):
        self.first = first
        self.second = second
        self.letter = letter
        self.password = password

    def matches_occurrence(self):
        num_letters = self.password.count(self.letter)
        return num_letters >= self.first and num_letters <= self.second

    def matches_position(self):
        letter1 = self.password[self.first - 1]
        letter2 = self.password[self.second - 1]
        return (letter1 == self.letter) ^ (letter2 == self.letter)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(3)

    def reset(self):
        self.map = []

    def input_line(self, line):
        self.map.append(line)

    def solve1(self):
        return str(self.trees_on_slope(3))
        trees = 0
        for y in range(0, len(self.map)):
            line = self.map[y]
            x = (y * 3) % len(line)
            if (line[x] == '#'):
                trees += 1
        return str(self.trees_on_slope(3))

    def solve2(self):
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        trees = 1
        for slope in slopes:
            trees *= self.trees_on_slope(slope[0], slope[1])
        return str(trees)

    def trees_on_slope(self, x_step, y_step = 1):
        trees = 0
        x = 0
        for y in range(0, len(self.map), y_step):
            line = self.map[y]
            if (line[x] == '#'):
                trees += 1
            x = (x + x_step) % len(line)
        return trees

r = runner()

r.test('Sample 1', [
    '..##.......',
    '#...#...#..',
    '.#....#..#.',
    '..#.#...#.#',
    '.#...##..#.',
    '..#.##.....',
    '.#.#.#....#',
    '.#........#',
    '#.##...#...',
    '#...##....#',
    '.#..#...#.#',
], '7', '336')

r.run()
