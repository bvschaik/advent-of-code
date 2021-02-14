import adventofcode
import re

class password_scrambler:
    def __init__(self, password):
        self.letters = list(password)

    def swap_position(self, x, y):
        tmp = self.letters[x]
        self.letters[x] = self.letters[y]
        self.letters[y] = tmp

    def swap_letter(self, x, y):
        self.swap_position(self.letters.index(x), self.letters.index(y))

    def rotate_left(self, amount):
        amount = amount % len(self.letters)
        self.letters = self.letters[amount:] + self.letters[0:amount]

    def rotate_right(self, amount):
        return self.rotate_left(len(self.letters) - amount)

    def rotate_letter(self, c):
        index = self.letters.index(c)
        times = 1 + index + (1 if index >= 4 else 0)
        self.rotate_right(times)

    def reverse_range(self, x, y):
        self.letters = self.letters[0:x] + list(reversed(self.letters[x:y+1])) + self.letters[y+1:]

    def move_position(self, from_pos, to_pos):
        c = self.letters[from_pos]
        del self.letters[from_pos]
        self.letters = self.letters[0:to_pos] + [c] + self.letters[to_pos:]

    def get_result(self):
        return ''.join(self.letters)

class password_unscrambler:
    def __init__(self, password):
        self.scrambler = password_scrambler(password)

    def swap_position(self, x, y):
        self.scrambler.swap_position(y, x)

    def swap_letter(self, x, y):
        self.scrambler.swap_letter(y, x)

    def rotate_left(self, amount):
        self.scrambler.rotate_right(amount)

    def rotate_right(self, amount):
        self.scrambler.rotate_left(amount)

    def rotate_letter(self, c):
        target_index = self.scrambler.letters.index(c)
        length = len(self.scrambler.letters)
        for index in range(length):
            times = 1 + index + (1 if index >= 4 else 0)
            if (index + times) % length == target_index:
                self.scrambler.rotate_left(times);
                return

    def reverse_range(self, x, y):
        self.scrambler.reverse_range(x, y)

    def move_position(self, from_pos, to_pos):
        self.scrambler.move_position(to_pos, from_pos)

    def get_result(self):
        return self.scrambler.get_result()

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(21)

    def reset(self):
        self.rules = []

    def input_line(self, line):
        if line.startswith('swap position'):
            m = re.match(r'swap position (\d+) with position (\d+)', line)
            self.rules.append(('swap_position', (int(m.group(1)), int(m.group(2)))))
        elif line.startswith('swap letter'):
            m = re.match(r'swap letter (.) with letter (.)', line)
            self.rules.append(('swap_letter', (m.group(1), m.group(2))))
        elif line.startswith('rotate based'):
            m = re.match(r'rotate based on position of letter (.)', line)
            self.rules.append(('rotate_letter', (m.group(1),)))
        elif line.startswith('rotate'):
            m = re.match(r'rotate (left|right) (\d+) steps?', line)
            self.rules.append(('rotate_' + m.group(1), (int(m.group(2)),)))
        elif line.startswith('reverse'):
            m = re.match(r'reverse positions (\d+) through (\d+)', line)
            self.rules.append(('reverse_range', (int(m.group(1)), int(m.group(2)))))
        elif line.startswith('move'):
            m = re.match(r'move position (\d+) to position (\d+)', line)
            self.rules.append(('move_position', (int(m.group(1)), int(m.group(2)))))
        else:
            print('unknown rule:', line)

    def solve1(self):
        pw = password_scrambler('abcdefgh')
        for rule in self.rules:
            func = getattr(pw, rule[0])
            func(*rule[1])
        return pw.get_result()

    def solve2(self):
        pw = password_unscrambler('fbgdceah')
        for rule in reversed(self.rules):
            func = getattr(pw, rule[0])
            func(*rule[1])
        return pw.get_result()

r = runner()
r.run()
