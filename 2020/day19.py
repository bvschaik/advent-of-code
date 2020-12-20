import adventofcode
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(19)

    def reset(self):
        self.rules = dict()
        self.messages = []

    def input_line(self, line):
        if ':' in line:
            m = re.match(r'(\d+): (.*)', line)
            rule_id = int(m.group(1))
            options = m.group(2).split(' | ')
            self.rules[rule_id] = []
            for group in options:
                if group[0] == '"':
                    self.rules[rule_id].append(group.strip('"'))
                else:
                    self.rules[rule_id].append(list(map(int, group.split(' '))))
        elif line:
            self.messages.append(line)

    def solve1(self):
        self.cache = dict()
        valids = self.find_valid(0)
        return str(sum(map(lambda m: m in valids, self.messages)))

    def find_valid(self, index):
        if index in self.cache:
            return self.cache[index]
        valids = set()
        for option in self.rules[index]:
            if len(option) == 1 and option[0] not in self.rules:
                valids.add(option[0])
                continue
            option_valids = set()
            for n in option:
                n_valids = self.find_valid(n)
                if option_valids:
                    new_valids = set()
                    for a in option_valids:
                        for b in n_valids:
                            new_valids.add(a + b)
                    option_valids = new_valids
                else:
                    option_valids = n_valids
            valids.update(option_valids)
        self.cache[index] = valids
        return valids

    def solve2(self):
        return str(sum(map(lambda m: self.is_valid_recursive(m), self.messages)))

    def is_valid_recursive(self, m):
        # knowledge:
        # 0 rule is always: 0: 8 11
        # 8 rule becomes 8: 42 | 42 8 -> rule 42 m times (n >= 1)
        # 11 rule becomes: 11: 42 31 | 42 11 31 -> rule 42 and 31 n times
        # -> 0 rule becomes: (m + n) * 42 + n * 31 (m and n >= 1)
        # 42 and 31 both result in 8-bit messages
        # 42 and 31 do not contain overlapping possibilities
        # So: split in 8-bit chunks and match those
        chunks = [m[start:start+8] for start in range(0, len(m), 8)]
        match42 = 0
        match31 = 0
        for c in chunks:
            if c in self.cache[42]:
                match42 += 1
            else:
                break
        for c in reversed(chunks):
            if c in self.cache[31]:
                match31 += 1
            else:
                break
        return match31 + match42 == len(chunks) and match42 > match31 and match31 > 0

r = runner()

r.test('Sample 1', [
    '0: 4 1 5',
    '1: 2 3 | 3 2',
    '2: 4 4 | 5 5',
    '3: 4 5 | 5 4',
    '4: "a"',
    '5: "b"',
    '',
    'ababbb',
    'bababa',
    'abbbab',
    'aaabbb',
    'aaaabbb',
], '2')

r.run()
