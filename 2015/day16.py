import adventofcode
import re

target_props = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(16)

    def reset(self):
        self.sues = dict()

    def input_line(self, line):
        m = re.match(r'Sue (\d+): (.*)', line)
        id = int(m.group(1))
        props = dict()
        for p in m.group(2).split(','):
            (key, value) = p.split(':')
            props[key.strip()] = int(value.strip())
        self.sues[id] = props

    def solve1(self):
        for n in self.sues:
            props = self.sues[n]
            match = True
            for p in props:
                if target_props[p] != props[p]:
                    match = False
                    break
            if match:
                return str(n)

    def solve2(self):
        for n in self.sues:
            props = self.sues[n]
            match = True
            for p in props:
                if p == 'cats' or p == 'trees':
                    if props[p] <= target_props[p]:
                        match = False
                elif p == 'pomeranians' or p == 'goldfish':
                    if props[p] >= target_props[p]:
                        match = False
                elif props[p] != target_props[p]:
                    match = False
                if not match:
                    break
            if match:
                return str(n)

r = runner()
r.run()
