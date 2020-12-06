import adventofcode

class group_type:
    def __init__(self):
        self.persons = []

    def add(self, value):
        self.persons.append(set(value))

    def union(self):
        answers = set()
        for p in self.persons:
            answers.update(p)
        return len(answers)

    def intersection(self):
        answers = self.persons[0]
        for p in self.persons:
            answers.intersection_update(p)
        return len(answers)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(6)

    def reset(self):
        self.groups = [group_type()]

    def input_line(self, line):
        if len(line) == 0:
            self.groups.append(group_type())
        else:
            group = self.groups[len(self.groups) - 1]
            group.add(line)

    def solve1(self):
        return str(sum(map(lambda g: g.union(), self.groups)))

    def solve2(self):
        return str(sum(map(lambda g: g.intersection(), self.groups)))

r = runner()

r.test('Sample 1', [
    'abc',
    '',
    'a',
    'b',
    'c',
    '',
    'ab',
    'ac',
    '',
    'a',
    'a',
    'a',
    'a',
    '',
    'b',
], '11', '6')

r.run()
