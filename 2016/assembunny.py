class computer:
    def __init__(self, instructions):
        self.reset()
        self.execute = {
            'inc': self.inc,
            'dec': self.dec,
            'cpy': self.cpy,
            'jnz': self.jnz,
            'tgl': self.tgl,
            'out': self.out,
            # Complex instructions
            'add': self.add,
            'mul': self.mul
        }
        self.instructions = []
        for instr in instructions:
            parts = instr.split(' ')
            args = tuple(map(lambda a: a if a in 'abcd' else int(a), parts[1:]))
            self.instructions.append([parts[0], args])

    def reset(self):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.ip = 0

    def inc(self, args):
        self.registers[args[0]] += 1
        self.ip += 1

    def dec(self, args):
        self.registers[args[0]] -= 1
        self.ip += 1

    def cpy(self, args):
        if args[1] in self.registers:
            self.registers[args[1]] = self.get_value(args[0])
        self.ip += 1

    def jnz(self, args):
        if self.get_value(args[0]):
            self.ip += self.get_value(args[1])
        else:
            self.ip += 1

    def tgl(self, args):
        offset = self.ip + self.get_value(args[0])
        self.ip += 1
        if offset < 0 or offset >= len(self.instructions):
            return
        instr = self.instructions[offset]
        if len(instr[1]) == 1:
            self.instructions[offset][0] = 'dec' if instr[0] == 'inc' else 'inc'
        else:
            self.instructions[offset][0] = 'cpy' if instr[0] == 'jnz' else 'jnz'

    def out(self, args):
        if self.output_func(self.get_value(args[0])):
            self.ip += 1
        else:
            self.ip = len(self.instructions)

    def add(self, args):
        self.registers[args[1]] += self.registers[args[0]]
        self.registers[args[0]] = 0
        self.ip += 3

    def mul(self, args):
        self.registers[args[0]] += self.get_value(args[1]) * self.registers[args[2]]
        self.registers[args[2]] = 0
        self.registers[args[3]] = 0
        self.ip += 6

    def get_value(self, arg):
        if isinstance(arg, str):
            return self.registers[arg]
        else:
            return arg

    def optimize_add(self):
        for i in range(len(self.instructions) - 2):
            if (self.instructions[i][0] == 'inc'
                and self.instructions[i+1][0] == 'dec'
                and self.instructions[i+2][0] == 'jnz'
                and self.instructions[i+1][1][0] == self.instructions[i+2][1][0]):
                # inc b
                # dec a
                # jnz a -2
                # --> this becomes: add a b --> b += a; a = 0
                reg_src = self.instructions[i+1][1][0]
                reg_dst = self.instructions[i][1][0]
                self.instructions[i] = ('add', (reg_src, reg_dst))
        return self

    def optimize_mul(self):
        for i in range(len(self.instructions) - 5):
            if (self.instructions[i][0] == 'cpy'
                and self.instructions[i+1][0] == 'inc'
                and self.instructions[i+2][0] == 'dec'
                and self.instructions[i+3][0] == 'jnz'
                and self.instructions[i+4][0] == 'dec'
                and self.instructions[i+5][0] == 'jnz'):
                # cpy b d
                # inc a
                # dec d
                # jnz d -2
                # dec c
                # jnz c
                # becomes:
                # a += b * c; c = 0; d = 0
                dst = self.instructions[i+1][1][0]
                op1 = self.instructions[i][1][0]
                op2 = self.instructions[i+5][1][0]
                nul = self.instructions[i][1][1]
                self.instructions[i] = ('mul', (dst, op1, op2, nul))
                # print('optimized', i, self.instructions[i])
        return self

    def run_until_end(self):
        max_ip = len(self.instructions)
        # counts = [0] * max_ip
        while self.ip < max_ip:
            # counts[self.ip] += 1
            (instr, args) = self.instructions[self.ip]
            self.execute[instr](args)
        # print(counts)

    def run_with_output(self):
        max_ip = len(self.instructions)
        while self.ip < max_ip:
            (instr, args) = self.instructions[self.ip]
            if instr == 'out':
                yield self.get_value(args[0])
                self.ip += 1
            else:
                self.execute[instr](args)
