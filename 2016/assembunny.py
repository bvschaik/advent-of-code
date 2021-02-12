class computer:
    def __init__(self, instructions):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.ip = 0
        self.execute = {
            'inc': self.inc,
            'dec': self.dec,
            'cpy_reg': self.cpy_reg,
            'cpy_val': self.cpy_val,
            'jnz_reg': self.jnz_reg,
            'jnz_val': self.jnz_val,
            # Complex instructions
            'add': self.add
        }
        self.instructions = []
        for instr in instructions:
            args = instr.split(' ')
            if len(args) == 2:
                self.instructions.append((args[0], (args[1])))
            elif args[1] in 'abcd':
                self.instructions.append(
                    (args[0] + '_reg', (args[1], args[2] if args[2] in 'abcd' else int(args[2])))
                )
            else:
                self.instructions.append(
                    (args[0] + '_val', (int(args[1]), args[2] if args[2] in 'abcd' else int(args[2])))
                )

    def inc(self, args):
        self.registers[args[0]] += 1
        self.ip += 1

    def dec(self, args):
        self.registers[args[0]] -= 1
        self.ip += 1

    def cpy_reg(self, args):
        self.registers[args[1]] = self.registers[args[0]]
        self.ip += 1

    def cpy_val(self, args):
        self.registers[args[1]] = args[0]
        self.ip += 1

    def jnz_reg(self, args):
        if self.registers[args[0]]:
            self.ip += args[1]
        else:
            self.ip += 1

    def jnz_val(self, args):
        if args[0]:
            self.ip += args[1]
        else:
            self.ip += 1

    def add(self, args):
        self.registers[args[1]] += self.registers[args[0]]
        self.registers[args[0]] = 0
        self.ip += 3

    def optimize_add(self):
        for i in range(len(self.instructions) - 2):
            if (self.instructions[i][0] == 'inc'
                and self.instructions[i+1][0] == 'dec'
                and self.instructions[i+2][0] == 'jnz_reg'
                and self.instructions[i+1][1][0] == self.instructions[i+2][1][0]):
                # inc b
                # dec a
                # jnz a -2
                # --> this becomes: add a b --> b += a; a = 0
                reg_src = self.instructions[i+1][1][0]
                reg_dst = self.instructions[i][1][0]
                self.instructions[i] = ('add', (reg_src, reg_dst))
        return self

    def run_until_end(self):
        max_ip = len(self.instructions)
        # counts = [0] * max_ip
        while self.ip < max_ip:
            # counts[self.ip] += 1
            (instr, args) = self.instructions[self.ip]
            self.execute[instr](args)
        # print(counts)
