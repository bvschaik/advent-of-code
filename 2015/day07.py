import adventofcode
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(7)

    def reset(self):
        self.instructions = dict()
        self.outputs = dict()

    def input_line(self, line):
        m = re.match(r'(.*) -> (.*)', line)
        instr = list(m.group(1).split(' '))
        output = m.group(2)
        self.instructions[output] = instr

    def solve1(self):
        return str(self.get_output('a'))

    def solve2(self):
        self.instructions['b'] = [str(self.outputs['a'])]
        self.outputs = dict()
        return str(self.get_output('a'))

    def get_output(self, wire):
        if wire.isdigit():
            return int(wire)
        if wire in self.outputs:
            return self.outputs[wire]

        instr = self.instructions[wire]
        if len(instr) == 1:
            result = self.get_output(instr[0])
        elif len(instr) == 2:
            if instr[0] == 'NOT':
                result = (~self.get_output(instr[1])) & 0xffff
        elif len(instr) == 3:
            v1 = self.get_output(instr[0])
            v2 = self.get_output(instr[2])
            if instr[1] == 'AND':
                result = v1 & v2
            elif instr[1] == 'OR':
                result = v1 | v2
            elif instr[1] == 'LSHIFT':
                result = v1 << v2
            elif instr[1] == 'RSHIFT':
                result = v1 >> v2

        self.outputs[wire] = result
        return result

r = runner()
r.run()
