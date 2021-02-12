import adventofcode
import re
from collections import deque

class bot:
    def __init__(self, name, low, high):
        self.name = name
        self.low = low
        self.high = high
        self.inputs = []

    def add_input(self, input):
        self.inputs.append(input)
        return len(self.inputs) == 2

    def process_inputs(self, queue):
        (low_value, high_value) = sorted(self.inputs)
        queue.append((self.low, low_value))
        queue.append((self.high, high_value))

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(10)

    def reset(self):
        self.values = []
        self.bots = dict()

    def input_line(self, line):
        if line.startswith('value'):
            m = re.match(r'value (\d+) goes to (.*)', line)
            self.values.append((m.group(2), int(m.group(1))))
        else:
            m = re.match(r'(.*) gives low to (.*) and high to (.*)', line)
            self.bots[m.group(1)] = bot(m.group(1), m.group(2), m.group(3))

    def solve1(self):
        queue = deque(self.values)
        outputs = dict()
        while queue:
            (id, value) = queue.pop()
            if id.startswith('bot'):
                b = self.bots[id]
                if b.add_input(value):
                    low, high = sorted(b.inputs)
                    if low == 17 and high == 61:
                        return id.split(' ')[1]
                    b.process_inputs(queue)

    def solve2(self):
        for b in self.bots.values():
            b.inputs.clear()

        queue = deque(self.values)
        outputs = dict()
        while queue:
            (id, value) = queue.pop()
            if id.startswith('output'):
                outputs[int(id.split(' ')[1])] = value
            else:
                b = self.bots[id]
                if b.add_input(value):
                    b.process_inputs(queue)

        return str(outputs[0] * outputs[1] * outputs[2])

r = runner()
r.run()
