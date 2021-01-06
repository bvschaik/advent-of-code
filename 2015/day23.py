import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(23)

    def reset(self):
        self.program = []

    def input_line(self, line):
        parts = line.split(' ')
        if len(parts) == 2:
            if parts[0] == 'jmp':
                self.program.append((parts[0], int(parts[1])))
            else:
                self.program.append((parts[0], parts[1]))
        elif len(parts) == 3:
            self.program.append((parts[0], parts[1].strip(','), int(parts[2])))

    def solve1(self):
        registers = {'a': 0, 'b': 0}
        return self.run_program(registers)

    def solve2(self):
        registers = {'a': 1, 'b': 0}
        return self.run_program(registers)

    def run_program(self, registers):
        instructions = self.program
        ip = 0
        max_ip = len(instructions)
        while ip >= 0 and ip < max_ip:
            instr = instructions[ip]
            if instr[0] == 'hlf':
                registers[instr[1]] //= 2
                ip += 1
            elif instr[0] == 'tpl':
                registers[instr[1]] *= 3
                ip += 1
            elif instr[0] == 'inc':
                registers[instr[1]] += 1
                ip += 1
            elif instr[0] == 'jmp':
                ip += instr[1]
            elif instr[0] == 'jie':
                if registers[instr[1]] % 2 == 0:
                    ip += instr[2]
                else:
                    ip += 1
            elif instr[0] == 'jio':
                if registers[instr[1]] == 1:
                    ip += instr[2]
                else:
                    ip += 1
        return str(registers['b'])

r = runner()
r.run()
