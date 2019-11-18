import re
from runner import runner

def exec_addr(a, b, c, registers):
    registers[c] = registers[a] + registers[b]

def exec_addi(a, b, c, registers):
    registers[c] = registers[a] + b

def exec_mulr(a, b, c, registers):
    registers[c] = registers[a] * registers[b]

def exec_muli(a, b, c, registers):
    registers[c] = registers[a] * b

def exec_banr(a, b, c, registers):
    registers[c] = registers[a] & registers[b]

def exec_bani(a, b, c, registers):
    registers[c] = registers[a] & b

def exec_borr(a, b, c, registers):
    registers[c] = registers[a] | registers[b]

def exec_bori(a, b, c, registers):
    registers[c] = registers[a] | b

def exec_setr(a, b, c, registers):
    registers[c] = registers[a]

def exec_seti(a, b, c, registers):
    registers[c] = a

def exec_gtir(a, b, c, registers):
    registers[c] = 1 if a > registers[b] else 0

def exec_gtri(a, b, c, registers):
    registers[c] = 1 if registers[a] > b else 0

def exec_gtrr(a, b, c, registers):
    registers[c] = 1 if registers[a] > registers[b] else 0

def exec_eqir(a, b, c, registers):
    registers[c] = 1 if a == registers[b] else 0

def exec_eqri(a, b, c, registers):
    registers[c] = 1 if registers[a] == b else 0

def exec_eqrr(a, b, c, registers):
    registers[c] = 1 if registers[a] == registers[b] else 0

def exec_div256(a, b, c, registers):
    registers[c] = registers[a] // 256
    registers[b] += 7

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
    'eqrr': exec_eqrr,
    'div256': exec_div256
}

class day21(runner):
    def __init__(self):
        self.ip = 0
        self.program = []

    def day(self):
        return 21

    def input(self, line):
        if line.startswith("#ip"):
            self.ip = int(line[4:])
        else:
            m = re.match(r"([^ ]+) (\d+) (\d+) (\d+)", line)
            self.program.append([m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))])

    def solve1(self):
        program = self.optimize_div256()
        # Register 0 is only consulted once in the program: to check whether
        # it's equal to some register's value. That value is our number.
        instr_referencing_r0 = list(filter(lambda x: x[0] == 'eqrr' and (x[1] == 0 or x[2] == 0), program))[0]
        check_register = instr_referencing_r0[1] if instr_referencing_r0[2] == 0 else instr_referencing_r0[2]
        instr_ip = program.index(instr_referencing_r0)

        ip_index = self.ip
        max_ip = len(program)
        registers = [0, 0, 0, 0, 0, 0]
        count = 0
        while registers[ip_index] >= 0 and registers[ip_index] < max_ip and registers[ip_index] != instr_ip:
            (instr, a, b, c) = program[registers[ip_index]]
            # print('ip=%d %s %s %d %d %d ' % (registers[ip_index], registers, instr, a, b, c), end = '')
            instructions[instr](a, b, c, registers)
            # print(registers)
            registers[ip_index] += 1
            count += 1

        return str(registers[check_register])

    def solve2(self):
        program = self.optimize_div256()
        # Register 0 is only consulted once in the program: to check whether
        # it's equal to some register's value. That value is our number.
        instr_referencing_r0 = list(filter(lambda x: x[0] == 'eqrr' and (x[1] == 0 or x[2] == 0), program))[0]
        check_register = instr_referencing_r0[1] if instr_referencing_r0[2] == 0 else instr_referencing_r0[2]
        instr_ip = program.index(instr_referencing_r0)

        # The value we're looking for is the last seen value before the first duplicate
        seen_values = set()
        last_value = 0

        ip_index = self.ip
        max_ip = len(program)
        registers = [0, 0, 0, 0, 0, 0]
        count = 0
        while registers[ip_index] >= 0 and registers[ip_index] < max_ip:
            if registers[ip_index] == instr_ip:
                value = registers[check_register]
                if value in seen_values:
                    return str(last_value)
                last_value = value
                seen_values.add(value)
            (instr, a, b, c) = program[registers[ip_index]]
            # print('ip=%d %s %s %d %d %d ' % (registers[ip_index], registers, instr, a, b, c), end = '')
            instructions[instr](a, b, c, registers)
            # print(registers)
            registers[ip_index] += 1
            count += 1

        return str(registers[check_register])

    def optimize_div256(self):
        program = list(self.program)
        for index in range(len(program)):
            if self.is_div256_instruction_set(program, index):
                # This calcalates: given P, put P / 256 in register Q
                p_register = program[index + 3][2]
                q_register = program[index][3]
                program[index] = ['div256', p_register, self.ip, q_register]
                # print("Optimized div256 at index", index)
        return program

    def is_div256_instruction_set(self, program, index):
        chain = ['seti', 'addi', 'muli', 'gtrr', 'addr', 'addi', 'seti', 'addi']
        if index + len(chain) > len(program):
            return False
        for delta, instr in enumerate(chain):
            if program[index + delta][0] != instr:
                return False
        return True

day21().solve()
