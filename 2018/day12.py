import re
from runner import runner

class day12(runner):
    base_offset = 100

    def __init__(self):
        self.state = []
        self.rules = [0] * 32

    def day(self):
        return 12

    def input(self, line):
        m = re.match(r"initial state: ([\.#]+)", line)
        if m:
            self.state = list(map(lambda x: 1 if x == '#' else 0, m.group(1)))
        else:
            m = re.match(r"([\.#]+) => ([\.#])", line)
            if m:
                index = sum(map(lambda x: 1 << (4 - x[0]) if x[1] == '#' else 0, enumerate(m.group(1))))
                self.rules[int(index)] = 1 if m.group(2) == '#' else 0

    def solve1(self):
        working_state = [0] * self.base_offset + self.state + [0] * 400

        for _ in range(0, 20):
            working_state = self.next_generation(working_state)
        
        return str(self.sum_plants_with_offset(working_state, -self.base_offset))

    def solve2(self):
        patterns = list()
        pattern_offsets = list()

        working_state = [0] * self.base_offset + self.state + [0] * 400
        for generation in range(0, 200):
            first_plant = working_state.index(1)
            last_plant = len(working_state) - 1 - working_state[::-1].index(1)
            pattern = working_state[first_plant:last_plant+1]
            if pattern in patterns:
                index = patterns.index(pattern)
                delta_offset = first_plant - pattern_offsets[index]
                target_generation = 50000000000
                generations_to_go = target_generation - generation
                return str(self.sum_plants_with_offset(working_state, generations_to_go * delta_offset - self.base_offset))
            patterns.append(pattern)
            pattern_offsets.append(first_plant)
            working_state = self.next_generation(working_state)
        pass

    def next_generation(self, working_state):
        value = working_state[0] << 1 + working_state[1]
        new_state = [0] * len(working_state)
        for i in range(2, len(working_state) - 2):
            value = ((value & 15) << 1) + working_state[i+2]
            new_state[i] = self.rules[value]
        return new_state

    def sum_plants_with_offset(self, pattern, offset):
        number_sum = 0
        for (i, val) in enumerate(pattern):
            if val == 1:
                number_sum += i + offset
        return number_sum

day12().solve()
