import re
from functools import partial
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

def exec_divisor(ip, p, q, r, registers):
    if registers[p] % registers[q] == 0:
        registers[r] += registers[q]
    registers[ip] += 9

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

class day19(runner):
    def __init__(self):
        self.ip = 0
        self.program = []
        self.optimization = None

    def day(self):
        return 19

    def input(self, line):
        if line.startswith("#ip"):
            self.ip = int(line[4:])
        else:
            m = re.match(r"([^ ]+) (\d+) (\d+) (\d+)", line)
            self.program.append([m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))])

    def solve1(self):
        self.optimize_divisor()
        count = 0
        ip_index = self.ip
        max_ip = len(self.program)
        registers = [0, 0, 0, 0, 0, 0]
        while registers[ip_index] >= 0 and registers[ip_index] < max_ip:
            (instr, a, b, c) = self.program[registers[ip_index]]
            #print('ip=%d %s %s %d %d %d ' % (registers[ip_index], registers, instr, a, b, c), end = '')
            instructions[instr](a, b, c, registers)
            #print(registers)
            registers[ip_index] += 1
            count += 1

        print(count)
        return str(registers[0])

    def solve2(self):
        self.optimize_divisor()
        count = 0
        ip_index = self.ip
        max_ip = len(self.program)
        registers = [1, 0, 0, 0, 0, 0]
        while registers[ip_index] >= 0 and registers[ip_index] < max_ip:
            (instr, a, b, c) = self.program[registers[ip_index]]
            #print('ip=%d %s %s %d %d %d ' % (registers[ip_index], registers, instr, a, b, c), end = '')
            instructions[instr](a, b, c, registers)
            #print(registers)
            registers[ip_index] += 1
            count += 1

        print(count)
        return str(registers[0])

    def optimize_divisor(self):
        for index in range(len(self.program)):
            if self.is_divisor_instruction_set(index):
                # This calcalates: given P and Q, if Q divides P (e.g. P % Q == 0), add Q to R
                p_register = self.program[index + 2][2]
                q_register = self.program[index + 1][1]
                r_register = self.program[index + 5][3]
                instructions['divisor'] = partial(exec_divisor, self.ip)
                self.program[index] = ['divisor', p_register, q_register, r_register]
                # print("Optimized divisor at index", index)

    def is_divisor_instruction_set(self, index):
        chain = ['seti', 'mulr', 'eqrr', 'addr', 'addi', 'addr', 'addi', 'gtrr', 'addr', 'seti']
        if index + len(chain) > len(self.program):
            return False
        for delta, instr in enumerate(chain):
            if self.program[index + delta][0] != instr:
                return False
        return True

day19().test('Sample input', [
    '#ip 0',
    'seti 5 0 1',
    'seti 6 0 2',
    'addi 0 1 0',
    'addr 1 2 3',
    'setr 1 0 0',
    'seti 8 0 4',
    'seti 9 0 5',
], '7')

day19().solve()
