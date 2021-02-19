import adventofcode
import assembunny

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(23)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        self.instructions.append(line)

    def solve1(self):
        comp = assembunny.computer(self.instructions)
        comp.registers['a'] = 7
        comp.optimize_mul()
        comp.run_until_end()
        return str(comp.registers['a'])

    def solve2(self):
        comp = assembunny.computer(self.instructions)
        comp.registers['a'] = 12
        comp.optimize_mul()
        comp.run_until_end()
        return str(comp.registers['a'])

r = runner()
r.run()
