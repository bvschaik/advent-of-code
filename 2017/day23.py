import adventofcode
from collections import defaultdict

class program:
    def __init__(self, program):
        self.program = program
        self.registers = defaultdict(int)
        self.ip = 0
        self.execute = {
            'set': self.set,
            'sub': self.sub,
            'mul': self.mul,
            'jnz': self.jnz
        }

    def set(self, x, y):
        self.registers[x] = self.get_value(y)
        self.ip += 1

    def sub(self, x, y):
        self.registers[x] -= self.get_value(y)
        self.ip += 1

    def mul(self, x, y):
        self.multiplications += 1
        self.registers[x] *= self.get_value(y)
        self.ip += 1

    def jnz(self, x, y):
        if self.get_value(x) != 0:
            self.ip += self.get_value(y)
        else:
            self.ip += 1

    def get_value(self, operand):
        if operand >= 'a' and operand <= 'h':
            return self.registers[operand]
        else:
            return int(operand)

    def run(self):
        self.multiplications = 0
        max_ip = len(self.program)
        while self.ip >= 0 and self.ip < max_ip:
            line = self.program[self.ip]
            self.execute[line[0]](line[1], line[2])
        return self.multiplications

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(23)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        self.instructions.append(line.split())

    def solve1(self):
        return str(program(self.instructions).run())

    def solve2(self):
        # What the assembly program does: determine if a number has divisors,
        # i.e. it is not a prime number
        b = int(self.instructions[0][-1])

        start = b * 100 + 100000
        end = start + 17000 + 1
        h = 0
        for n in range(start, end, 17):
            if self.has_divisors(n):
                h += 1

        return str(h)

    def has_divisors(self, n):
        d = 2
        while d * d <= n:
            if n % d == 0:
                return True
            d += 1
        return False

r = runner()
r.run()
