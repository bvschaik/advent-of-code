import adventofcode
import re
from collections import defaultdict

class plant_configuration:
    def __init__(self, configuration, offset):
        while configuration.startswith('.....'):
            configuration = configuration[1:]
            offset += 1
        while not configuration.startswith('....'):
            configuration = '.' + configuration
            offset -= 1
        while configuration.endswith('......'):
            configuration = configuration[:-1]
        while not configuration.endswith('....'):
            configuration += '.'
        self.configuration = configuration
        self.offset = offset

    def next_generation(self, rules):
        new_config = []
        for i in range(len(self.configuration) - 4):
            new_config.append(rules[self.configuration[i:i+5]])
        return plant_configuration(''.join(new_config), self.offset + 2)

    def sum_plants(self):
        return self.sum_plants_with_offset(self.offset)

    def sum_plants_with_offset(self, offset):
        number_sum = 0
        for (i, val) in enumerate(self.configuration):
            if val == '#':
                number_sum += i + offset
        return number_sum

    def __repr__(self):
        return self.configuration + " " + str(self.offset)

def dot():
    return '.'

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(12)

    def reset(self):
        self.state = []
        self.rules = defaultdict(dot)

    def input_line(self, line):
        m = re.match(r"initial state: ([\.#]+)", line)
        if m:
            self.state = m.group(1)
        else:
            m = re.match(r"([\.#]+) => ([\.#])", line)
            if m:
                self.rules[m.group(1)] = m.group(2)

    def solve1(self):
        working_state = plant_configuration(self.state, 0)

        for _ in range(20):
            working_state = working_state.next_generation(self.rules)
        
        return str(working_state.sum_plants())

    def solve2(self):
        configurations = list()
        patterns_lookup = dict()

        working_state = plant_configuration(self.state, 0)
        generation = 0
        while True:
            if working_state.configuration in patterns_lookup:
                prev_generation = patterns_lookup[working_state.configuration]
                prev_state = configurations[prev_generation]
                delta_offset = working_state.offset - prev_state.offset
                target_generation = 50000000000
                generations_to_go = target_generation - generation
                return str(working_state.sum_plants_with_offset(generations_to_go * delta_offset + working_state.offset))
            configurations.append(working_state)
            patterns_lookup[working_state.configuration] = generation
            generation += 1
            working_state = working_state.next_generation(self.rules)

r = runner()
r.test('Sample input', [
    'initial state: #..#.#..##......###...###',
    '...## => #',
    '..#.. => #',
    '.#... => #',
    '.#.#. => #',
    '.#.## => #',
    '.##.. => #',
    '.#### => #',
    '#.#.# => #',
    '#.### => #',
    '##.#. => #',
    '##.## => #',
    '###.. => #',
    '###.# => #',
    '####. => #',
], '325')

r.run()
