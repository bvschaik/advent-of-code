import adventofcode

class instruction:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.executed = False

    def run(self, program):
        if self.name == 'acc':
            program.accumulator += self.value
        elif self.name == 'jmp':
            program.ip += self.value - 1
        program.ip += 1
        self.executed = True

class program:
    def __init__(self):
        self.instructions = []
        self.ip = 0
        self.accumulator = 0

    def add_instruction(self, name, value):
        self.instructions.append(instruction(name, value))

    def run(self):
        self.clear()
        max_ip = len(self.instructions)
        instr = self.instructions[0]
        while not instr.executed:
            instr.run(self)
            if self.ip == max_ip:
                return (True, self.accumulator)
            if self.ip < 0 or self.ip > max_ip:
                break
            instr = self.instructions[self.ip]
        return (False, self.accumulator)

    def clear(self):
        self.ip = 0
        self.accumulator = 0
        for i in self.instructions:
            i.executed = False

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(8)

    def reset(self):
        self.program = program()

    def input_line(self, line):
        (name, value) = line.split()
        self.program.add_instruction(name, int(value))

    def solve1(self):
        (ok, acc) = self.program.run()
        return str(acc)

    def solve2(self):
        for (index, instr) in enumerate(self.program.instructions):
            if instr.name == 'acc':
                continue
            elif instr.name == 'jmp':
                self.program.instructions[index] = instruction('nop', instr.value)
            elif instr.name == 'nop':
                self.program.instructions[index] = instruction('jmp', instr.value)
            (ok, acc) = self.program.run()
            self.program.instructions[index] = instr
            if ok:
                return str(acc)

r = runner()

r.test('Sample 1', [
    'nop +0',
    'acc +1',
    'jmp +4',
    'acc +3',
    'jmp -3',
    'acc -99',
    'acc +1',
    'jmp -4',
    'acc +6',
], '5', '8')

r.run()
