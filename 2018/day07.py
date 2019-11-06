import re
import heapq
from runner import runner

class step:
    def __init__(self, id):
        self.id = id
        self.needs = list()
        self.is_needed_for = list()
        self.done = False

    def can_do(self):
        for s in self.needs:
            if not s.done:
                return False
        return True

    def name(self):
        return chr(self.id + ord('A'))

    def __repr__(self):
        return str(self.id)

def name_to_index(letter):
    return ord(letter) - ord('A')

class day07(runner):
    def __init__(self, part2_threshold = 10000):
        self.steps = [None] * 26

    def day(self):
        return 7
    
    def input(self, line):
        m = re.match(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.', line)
        from_step = self.get_step(m.group(1))
        to_step = self.get_step(m.group(2))
        from_step.is_needed_for.append(to_step)
        to_step.needs.append(from_step)

    def get_step(self, name):
        index = name_to_index(name)
        if self.steps[index] is None:
            self.steps[index] = step(index)
        return self.steps[index]

    def solve1(self):
        h = []
        for s in self.steps:
            if s is not None and not s.needs:
                heapq.heappush(h, (s.id, s))
        
        order = []
        while len(h) > 0:
            (_, s) = heapq.heappop(h)
            s.done = True
            order.append(s.name())
            for dep_step in s.is_needed_for:
                if dep_step.can_do():
                    heapq.heappush(h, (dep_step.id, dep_step))

        return "".join(order)

    def solve2(self):
        pass

day07().test('Sample input', [
    'Step C must be finished before step A can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step B can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step D must be finished before step E can begin.',
    'Step F must be finished before step E can begin.'
], 'CABDFE')

day07().solve()
