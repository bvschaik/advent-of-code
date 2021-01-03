import adventofcode
import re

def is_register(n):
    return n >= 0 and n < 4

def exec_addr(a, b, c, registers):
    if is_register(a) and is_register(b):
        registers[c] = registers[a] + registers[b]
        return True
    return False

def exec_addi(a, b, c, registers):
    if is_register(a):
        registers[c] = registers[a] + b
        return True
    return False

def exec_mulr(a, b, c, registers):
    if is_register(a) and is_register(b):
        registers[c] = registers[a] * registers[b]
        return True
    return False

def exec_muli(a, b, c, registers):
    if is_register(a):
        registers[c] = registers[a] * b
        return True
    return False

def exec_banr(a, b, c, registers):
    if is_register(a) and is_register(b):
        registers[c] = registers[a] & registers[b]
        return True
    return False

def exec_bani(a, b, c, registers):
    if is_register(a):
        registers[c] = registers[a] & b
        return True
    return False

def exec_borr(a, b, c, registers):
    if is_register(a) and is_register(b):
        registers[c] = registers[a] | registers[b]
        return True
    return False

def exec_bori(a, b, c, registers):
    if is_register(a):
        registers[c] = registers[a] | b
        return True
    return False

def exec_setr(a, b, c, registers):
    if is_register(a):
        registers[c] = registers[a]
        return True
    return False

def exec_seti(a, b, c, registers):
    registers[c] = a
    return True

def exec_gtir(a, b, c, registers):
    if is_register(b):
        registers[c] = 1 if a > registers[b] else 0
        return True
    return False

def exec_gtri(a, b, c, registers):
    if is_register(a):
        registers[c] = 1 if registers[a] > b else 0
        return True
    return False

def exec_gtrr(a, b, c, registers):
    if is_register(a) and is_register(b):
        registers[c] = 1 if registers[a] > registers[b] else 0
        return True
    return False

def exec_eqir(a, b, c, registers):
    if is_register(b):
        registers[c] = 1 if a == registers[b] else 0
        return True
    return False

def exec_eqri(a, b, c, registers):
    if is_register(a):
        registers[c] = 1 if registers[a] == b else 0
        return True
    return False

def exec_eqrr(a, b, c, registers):
    if is_register(a) and is_register(b):
        registers[c] = 1 if registers[a] == registers[b] else 0
        return True
    return False

instructions = {
    'addr': exec_addr,
    'addi': exec_addi,
    'mulr': exec_mulr,
    'muli': exec_muli,
    'banr': exec_banr,
    'bani': exec_bani,
    'borr': exec_borr,
    'bori': exec_bori,
    'setr': exec_setr,
    'seti': exec_seti,
    'gtir': exec_gtir,
    'gtri': exec_gtri,
    'gtrr': exec_gtrr,
    'eqir': exec_eqir,
    'eqri': exec_eqri,
    'eqrr': exec_eqrr
}

class sample:
    def __init__(self):
        self.before = None
        self.after = None
        self.instruction = None

    def __repr__(self):
        return str.format("%s => %s with %s" % (self.before, self.after, self.instruction))

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(16)

    def reset(self):
        self.samples = []
        self.program = []
        self.incomplete_sample = None

    def input_line(self, line):
        if len(line) == 0:
            return
        m = re.search(r"(\d+),? (\d+),? (\d+),? (\d+)", line)
        if not m:
            print("Line does not match:", line)
            return
        numbers = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
        if line.startswith("Before"):
            self.incomplete_sample = sample()
            self.incomplete_sample.before = numbers
        elif line.startswith("After"):
            self.incomplete_sample.after = numbers
            self.samples.append(self.incomplete_sample)
            self.incomplete_sample = None
        elif self.incomplete_sample:
            self.incomplete_sample.instruction = numbers
        else:
            self.program.append(numbers)

    def solve1(self):
        sample_count = 0
        for s in self.samples:
            count = 0
            (_, a, b, c) = s.instruction
            for exe in instructions.values():
                output = list(s.before)
                if exe(a, b, c, output) and output == s.after:
                    count += 1
            if count >= 3:
                sample_count += 1
        return str(sample_count)

    def solve2(self):
        mapping = self.find_mapping()
        registers = [0, 0, 0, 0]
        for (opco, a, b, c) in self.program:
            instructions[mapping[opco]](a, b, c, registers)
        return str(registers[0])

    def find_mapping(self):
        # Find all possible instructions for each opco
        opco_to_instr = dict()
        for s in self.samples:
            (opco, a, b, c) = s.instruction
            possible_opcos = set()
            for (instr, exe) in instructions.items():
                output = list(s.before)
                if exe(a, b, c, output) and output == s.after:
                    possible_opcos.add(instr)
            if opco in opco_to_instr:
                opco_to_instr[opco] = opco_to_instr[opco] & possible_opcos
            else:
                opco_to_instr[opco] = possible_opcos
        # Now try to figure out which opco maps to which instruction: if there's
        # one instruction possible, take it, and remove it from the other opcos
        taken_instr = set()
        final_mapping = [None] * 16
        while len(taken_instr) < 16:
            for opco in opco_to_instr.keys():
                opco_to_instr[opco] -= taken_instr
                if len(opco_to_instr[opco]) == 1:
                    instr = opco_to_instr[opco].pop()
                    final_mapping[opco] = instr
                    taken_instr.add(instr)
        return final_mapping

r = runner()
r.test('Sample input', [
    'Before: [3, 2, 1, 1]',
    '9 2 1 2',
    'After:  [3, 2, 2, 1]',
], '1')

r.run()
