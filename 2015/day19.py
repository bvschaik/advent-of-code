import adventofcode
import re

def find_all_substrings(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1:
            return
        yield start
        start += 1

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(19)

    def reset(self):
        self.reactions = dict()
        self.medicine = None

    def input_line(self, line):
        if not line:
            return
        if line.find(' => ') != -1:
            parts = line.split(' ')
            elem_from = parts[0]
            elem_to = parts[2]
            if elem_from not in self.reactions:
                self.reactions[elem_from] = []
            self.reactions[elem_from].append(elem_to)
        else:
            self.medicine = line

    def solve1(self):
        all_results = self.react(self.medicine)
        return str(len(all_results))

    def react(self, element):
        all_results = set()
        for e_from in self.reactions:
            for index in find_all_substrings(element, e_from):
                first = element[0:index]
                last = element[index + len(e_from):]
                for e_to in self.reactions[e_from]:
                    all_results.add(first + e_to + last)
        return all_results

    def solve2(self):
        # All reactions are of one of these forms:
        # 1. A -> B C (for any A, B, C; 1 element forms in 1 reaction)
        # 2. A -> B Rn C Ar (for any A, B, C; 3 elements form in 1 reaction)
        # 3. A -> B Rn C Y D Ar (for any A, B, C, D; 5 elements form in 1 reaction)
        # 4. A -> B RN C Y D Y E Ar (for any A, B, C, D, E; 7 elements form in 1 reaction)
        # Rn, Y, Ar are inert, so the ones present in the medicine are all there have been formed
        # -> Each Y contributes 2 additional elements every step
        # -> Each Rn contributes 2 additional elements every step
        # -> One token should be left at the end: -1

        num_elements = len(re.findall(r'[A-Z]', self.medicine))
        num_Y = len(re.findall('Y', self.medicine))
        num_Rn = len(re.findall('Rn', self.medicine))
        total_reactions = num_elements - 2 * (num_Y + num_Rn) - 1
        return str(total_reactions)

r = runner()

r.test('Sample', [
    'H => HO',
    'H => OH',
    'O => HH',
    '',
    'HOH'
], '4')

r.run()
