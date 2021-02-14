import adventofcode
import hashlib
from collections import deque

SIZE = 4
VAULT_X = 3
VAULT_Y = 3

DIRECTIONS = [0, 1, 2, 3]
DIR_LETTERS = ['U', 'D', 'L', 'R']
DIR_VALUES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

class path:
    def __init__(self, key, path, x, y):
        self.key = key
        self.path = path
        self.x = x
        self.y = y
        digest = hashlib.md5((key + path).encode('utf-8')).digest()
        up = (digest[0] & 0xf0) >> 4
        down = digest[0] & 0xf
        left = (digest[1] & 0xf0) >> 4
        right = digest[1] & 0xf
        self.doors = [
            y > 0 and up > 10,
            y + 1 < SIZE and down > 10,
            x > 0 and left > 10,
            x + 1 < SIZE and right > 10
        ]

    def is_target(self):
        return self.x == VAULT_X and self.y == VAULT_Y

    def can_move(self, direction):
        return self.doors[direction]

    def move(self, direction):
        return path(self.key, self.path + DIR_LETTERS[direction],
            self.x + DIR_VALUES[direction][0], self.y + DIR_VALUES[direction][1])

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(17)

    def reset(self):
        self.key = None

    def input_line(self, line):
        self.key = line

    def solve1(self):
        p = self.find_shortest_path()
        return p

    def solve2(self):
        p = self.find_longest_path()
        return str(len(p))

    def find_shortest_path(self):
        queue = deque()
        queue.append(path(self.key, '', 0, 0))
        while queue:
            p = queue.popleft()
            if p.is_target():
                return p.path
            else:
                for d in DIRECTIONS:
                    if p.can_move(d):
                        queue.append(p.move(d))

    def find_longest_path(self):
        longest = ''
        queue = deque()
        queue.append(path(self.key, '', 0, 0))
        while queue:
            p = queue.popleft()
            if p.is_target():
                # It's breadth-first search, so any later path found is >= previous path
                longest = p.path
            else:
                for d in DIRECTIONS:
                    if p.can_move(d):
                        queue.append(p.move(d))
        return longest

r = runner()
r.run()
