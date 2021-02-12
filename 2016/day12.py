import adventofcode
import assembunny

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(12)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        self.instructions.append(line)

    def solve1(self):
        comp = assembunny.computer(self.instructions).optimize_add()
        comp.run_until_end()
        return str(comp.registers['a'])

    def solve2(self):
        comp = assembunny.computer(self.instructions).optimize_add()
        comp.registers['c'] = 1
        comp.run_until_end()
        return str(comp.registers['a'])

r = runner()
r.run()
