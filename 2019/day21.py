import adventofcode
import intcode

NOT = 'NOT'
AND = 'AND'
OR = 'OR'
J = 5
REGISTERS = ['A', 'B', 'C', 'D', 'T', 'J']

class springscript:
    def __init__(self):
        self.instructions = []

    def write_line(self, line):
        i, a, b = line.split(' ')
        self.instructions.append((i, REGISTERS.index(a), REGISTERS.index(b)))

    def run(self, a, b, c, d):
        registers = [a, b, c, d, False, False]
        for i, r1, r2 in self.instructions:
            if i == NOT:
                registers[r2] = not registers[r1]
            elif i == AND:
                registers[r2] = registers[r1] and registers[r2]
            elif i == OR:
                registers[r2] = registers[r1] or registers[r2]
        return registers[J]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(21)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computer = intcode.ascii_computer(self.data)
        print(computer.read_line())

        computer.write_line('NOT B J')
        computer.write_line('NOT C T')
        computer.write_line('OR T J')
        computer.write_line('AND D J')
        computer.write_line('NOT A T')
        computer.write_line('OR T J')

        computer.write_line('WALK')

        for line in computer.lines():
            print(line)

        return str(computer.output[-1])

    def solve2(self):
        pass

computer = springscript()
computer.write_line('NOT B J')
computer.write_line('NOT C T')
computer.write_line('OR T J')
computer.write_line('AND D J')
computer.write_line('NOT A T')
computer.write_line('OR T J')

for a in [True, False]:
    for b in [True, False]:
        for c in [True, False]:
            for d in [True, False]:
                result = computer.run(a, b, c, d)
                print('#' if a else '.', end = '')
                print('#' if b else '.', end = '')
                print('#' if c else '.', end = '')
                print('#' if d else '.', end = '')
                print('  jump' if result else '  walk')

r = runner()
r.run()
