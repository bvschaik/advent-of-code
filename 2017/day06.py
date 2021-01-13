import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(6)

    def reset(self):
        self.inputs = []

    def input_line(self, line):
        self.inputs = list(map(int, line.split()))

    def solve1(self):
        memory = list(self.inputs)
        configurations = set()
        configurations.add(tuple(memory))
        steps = 0
        while True:
            steps += 1
            self.redistribute(memory)
            config = tuple(memory)
            if config in configurations:
                self.duplicate_config = config
                return str(steps)
            else:
                configurations.add(config)

    def redistribute(self, memory):
        max_index = 0
        max_n = 0
        for i, n in enumerate(memory):
            if n > max_n:
                max_n = n
                max_index = i
        max_memory = len(memory)
        add_to_all = max_n // max_memory
        one_for_some = max_n % max_memory
        memory[max_index] = 0
        for i in range(max_memory):
            memory[i] += add_to_all
        for i in range(one_for_some):
            memory[(max_index + i + 1) % max_memory] += 1

    def solve2(self):
        memory = list(self.duplicate_config)
        steps = 0
        while True:
            steps += 1
            self.redistribute(memory)
            config = tuple(memory)
            if config == self.duplicate_config:
                return str(steps)

r = runner()

r.test('Sample', [
    '0 2 7 0',
], '5', '0')

r.run()
