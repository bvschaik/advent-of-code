import adventofcode
import re
import heapq

class step:
    def __init__(self, id):
        self.id = id
        self.needs = list()
        self.is_needed_for = list()
        self.done = False
        self.done_time = 0

    def can_do(self):
        for s in self.needs:
            if not s.done:
                return False
        return True

    def dependencies_done_at(self):
        return max(map(lambda s: s.done_time, self.needs), default = 0)

    def name(self):
        return chr(self.id + ord('A'))

    def __repr__(self):
        return str(self.id)

def name_to_index(letter):
    return ord(letter) - ord('A')

class worker:
    def __init__(self):
        self.available_at = 0

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(7)

    def configure(self, num_workers = 5, base_task_duration = 61):
        self.base_task_duration = base_task_duration
        self.workers = [worker() for _ in range(num_workers)]

    def reset(self):
        self.steps = [None] * 26

    def input_line(self, line):
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
        h = []
        for s in self.steps:
            if s is not None:
                s.done = False
                if not s.needs:
                    heapq.heappush(h, ((0, s.id), s))
        
        while len(h) > 0:
            ((time, _), s) = heapq.heappop(h)
            step_time = self.base_task_duration + s.id
            worker = self.next_available_worker()
            worker.available_at = max(worker.available_at, time) + step_time
            s.done = True
            s.done_time = worker.available_at
            for dep_step in s.is_needed_for:
                if dep_step.can_do():
                    heapq.heappush(h, ((dep_step.dependencies_done_at(), dep_step.id), dep_step))

        return str(max(self.workers, key = lambda w: w.available_at).available_at)

    def next_available_worker(self):
        return min(self.workers, key = lambda w: w.available_at)

r = runner()

# r.configure(2, 61)
r.configure(num_workers = 2, base_task_duration = 1)
r.test('Sample input', [
    'Step C must be finished before step A can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step B can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step D must be finished before step E can begin.',
    'Step F must be finished before step E can begin.'
], 'CABDFE', '15')

r.configure()
r.run()
