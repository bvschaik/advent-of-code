import adventofcode
import re
from collections import defaultdict

class instruction:
    def __init__(self, reg, action, value, cond_left, cond_oper, cond_right):
        self.reg = reg
        self.action = action
        self.value = value
        self.cond_left = cond_left
        self.cond_oper = cond_oper
        self.cond_right = cond_right

    def apply(self, registers):
        if self.evaluate_condition(registers):
            self.perform_action(registers)
        return registers[self.reg]

    def evaluate_condition(self, registers):
        v1 = registers[self.cond_left]
        v2 = self.cond_right
        if self.cond_oper == '==':
            return v1 == v2
        elif self.cond_oper == '!=':
            return v1 != v2
        elif self.cond_oper == '<=':
            return v1 <= v2
        elif self.cond_oper == '<':
            return v1 < v2
        elif self.cond_oper == '>=':
            return v1 >= v2
        elif self.cond_oper == '>':
            return v1 > v2

    def perform_action(self, registers):
        diff = self.value if self.action == 'inc' else -self.value
        registers[self.reg] += diff

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(8)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        m = re.match(r'(.*) (inc|dec) (.*) if (.*) (.*) (.*)', line)
        self.instructions.append(instruction(
            m.group(1), m.group(2), int(m.group(3)),
            m.group(4), m.group(5), int(m.group(6))
        ))

    def solve1(self):
        registers = defaultdict(int)
        for i in self.instructions:
            i.apply(registers)
        return str(max(registers.values()))

    def solve2(self):
        registers = defaultdict(int)
        max_value = 0
        for i in self.instructions:
            max_value = max(max_value, i.apply(registers))
        return str(max_value)

r = runner()
r.run()
