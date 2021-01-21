import adventofcode
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(24)

    def reset(self):
        self.dominos = []

    def input_line(self, line):
        self.dominos.append(tuple(map(int, line.split('/'))))

    def solve1(self):
        self.by_value = defaultdict(set)
        for i, d in enumerate(self.dominos):
            self.by_value[d[0]].add(i)
            self.by_value[d[1]].add(i)

        all_dominos = set(range(len(self.dominos)))
        return str(self.recurse1(0, all_dominos))

    def recurse1(self, plug, available):
        max_strength = 0
        for n in self.by_value[plug]:
            if n in available:
                d = self.dominos[n]
                other_plug = d[1] if d[0] == plug else d[0]
                available.remove(n)
                strength = plug + other_plug + self.recurse1(other_plug, available)
                if strength > max_strength:
                    max_strength = strength
                available.add(n)
        return max_strength

    def solve2(self):
        self.max_depth = 0
        self.max_strength = 0
        all_dominos = set(range(len(self.dominos)))
        self.recurse2(0, all_dominos, 0, 0)
        return str(self.max_strength)

    def recurse2(self, plug, available, strength, depth):
        if depth > self.max_depth:
            self.max_depth = depth
            self.max_strength = strength
        elif depth == self.max_depth and strength > self.max_strength:
            self.max_strength = strength
        for n in self.by_value[plug]:
            if n in available:
                d = self.dominos[n]
                other_plug = d[1] if d[0] == plug else d[0]
                available.remove(n)
                self.recurse2(other_plug, available, strength + plug + other_plug, depth + 1)
                available.add(n)

r = runner()
r.run()
