import adventofcode
import re
from collections import deque

class bag_type:
    def __init__(self, name, contains):
        self.name = name
        self.contains = contains
        self.contained_in = []

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(7)

    def reset(self):
        self.bags = dict()

    def input_line(self, line):
        m = re.match(r'([^ ]+ [^ ]+) bags contain (.*)\.', line)
        name = m.group(1)
        contains = []
        if m.group(2) != 'no other bags':
            inner = []
            for bag in m.group(2).split(", "):
                (amount, color1, color2, _) = bag.split(" ")
                contains.append((int(amount), color1 + " " + color2))
        self.bags[name] = bag_type(name, contains)

    def solve1(self):
        for bag in self.bags.values():
            for contain in bag.contains:
                self.bags[contain[1]].contained_in.append(bag)
        queue = deque([self.bags['shiny gold']])
        colors = set()
        while queue:
            bag = queue.popleft()
            for x in bag.contained_in:
                queue.append(x)
                colors.add(x.name)
        return str(len(colors))

    def solve2(self):
        # Minus one for the shiny bag itself
        return str(self.count_bags(self.bags['shiny gold']) - 1)

    def count_bags(self, bag):
        return 1 + sum(map(lambda bag: bag[0] * self.count_bags(self.bags[bag[1]]), bag.contains))

r = runner()

r.test('Sample 1', [
    'light red bags contain 1 bright white bag, 2 muted yellow bags.',
    'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
    'bright white bags contain 1 shiny gold bag.',
    'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
    'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
    'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
    'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
    'faded blue bags contain no other bags.',
    'dotted black bags contain no other bags.',
], '4', '32')

r.run()
