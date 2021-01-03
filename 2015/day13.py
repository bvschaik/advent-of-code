import adventofcode
import re

INFINITY = 1000000

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(13)

    def reset(self):
        self.matrix = dict()

    def input_line(self, line):
        m = re.match(r'(.*) would (lose|gain) (\d+) happiness units by sitting next to (.*).', line)
        p1 = m.group(1)
        p2 = m.group(4)
        happiness = int(m.group(3))
        if m.group(2) == 'lose':
            happiness = -happiness
        if not p1 in self.matrix:
            self.matrix[p1] = dict()
        self.matrix[p1][p2] = happiness

    def solve1(self):
        all_persons = set(self.matrix.keys())
        random_person = all_persons.pop()
        happiness = self.visit_max(random_person, all_persons, random_person)
        return str(happiness)

    def solve2(self):
        # Add "Myself" to matrix
        all_persons = set(self.matrix.keys())
        me = "Myself"
        self.matrix[me] = dict()
        for p in all_persons:
            self.matrix[me][p] = 0
            self.matrix[p][me] = 0
        happiness = self.visit_max(me, all_persons, me)
        return str(happiness)

    def visit_max(self, start_person, other_persons, end_person):
        if len(other_persons) == 0:
            return self.matrix[start_person][end_person] + self.matrix[end_person][start_person]
        max_happiness = 0
        for p in other_persons:
            happiness = self.matrix[start_person][p] + self.matrix[p][start_person] + self.visit_max(p, other_persons - {p}, end_person)
            if happiness > max_happiness:
                max_happiness = happiness
        return max_happiness

r = runner()

r.test('Sample', [
    'Alice would gain 54 happiness units by sitting next to Bob.',
    'Alice would lose 79 happiness units by sitting next to Carol.',
    'Alice would lose 2 happiness units by sitting next to David.',
    'Bob would gain 83 happiness units by sitting next to Alice.',
    'Bob would lose 7 happiness units by sitting next to Carol.',
    'Bob would lose 63 happiness units by sitting next to David.',
    'Carol would lose 62 happiness units by sitting next to Alice.',
    'Carol would gain 60 happiness units by sitting next to Bob.',
    'Carol would gain 55 happiness units by sitting next to David.',
    'David would gain 46 happiness units by sitting next to Alice.',
    'David would lose 7 happiness units by sitting next to Bob.',
    'David would gain 41 happiness units by sitting next to Carol.',
], '330')

r.run()
