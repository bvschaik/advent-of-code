from collections import defaultdict

class computer:
    def __init__(self, program, input = []):
        self.program = defaultdict(int)
        for i, x in enumerate(program):
            self.program[i] = x
        self.ip = 0
        self.relative_base = 0
        self.running = True
        self.input = input
        self.output = []
        self.opcodes = {
            1: self.add,
            2: self.multiply,
            3: self.read_input,
            4: self.write_output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.adjust_relative_base,
            99: self.exit
        }

    def run(self):
        while self.running:
            code = self.program[self.ip]
            opcode = code % 100
            modes = code // 100
            self.opcodes[opcode](modes)

    def run_until_output(self):
        while self.running:
            code = self.program[self.ip]
            opcode = code % 100
            modes = code // 100
            self.opcodes[opcode](modes)
            if opcode == 4:
                return self.output[-1]
        return None

    def run_until_io(self):
        while self.running:
            code = self.program[self.ip]
            opcode = code % 100
            modes = code // 100
            if opcode == 3 and not self.input:
                return 'input'
            self.opcodes[opcode](modes)
            if opcode == 4:
                return 'output'
        return None

    def iterator(self, input_func = None):
        while self.running:
            code = self.program[self.ip]
            opcode = code % 100
            modes = code // 100
            if opcode == 3 and input_func and not self.input:
                input_func(self)
            self.opcodes[opcode](modes)
            if opcode == 4:
                yield self.output[-1]

    def iterator_triple(self, input_func = None):
        return zip(*(self.iterator(input_func),) * 3)

    def add(self, modes):
        val_a = self.get_value(1, modes)
        val_b = self.get_value(2, modes)
        reg_c = self.get_register(3, modes)
        self.set_value(reg_c, val_a + val_b)
        self.ip += 4

    def multiply(self, modes):
        val_a = self.get_value(1, modes)
        val_b = self.get_value(2, modes)
        reg_c = self.get_register(3, modes)
        self.set_value(reg_c, val_a * val_b)
        self.ip += 4

    def read_input(self, modes):
        reg_a = self.get_register(1, modes)
        if not self.input:
            raise AssertionError("Attempting to read input but input is empty?!")
        self.set_value(reg_a, self.input.pop(0))
        self.ip += 2

    def write_output(self, modes):
        val = self.get_value(1, modes)
        self.output.append(val)
        self.ip += 2

    def jump_if_true(self, modes):
        val = self.get_value(1, modes)
        if val:
            self.ip = self.get_value(2, modes)
        else:
            self.ip += 3

    def jump_if_false(self, modes):
        val = self.get_value(1, modes)
        if val == 0:
            self.ip = self.get_value(2, modes)
        else:
            self.ip += 3

    def less_than(self, modes):
        val_a = self.get_value(1, modes)
        val_b = self.get_value(2, modes)
        reg_c = self.get_register(3, modes)
        self.set_value(reg_c, 1 if val_a < val_b else 0)
        self.ip += 4

    def equals(self, modes):
        val_a = self.get_value(1, modes)
        val_b = self.get_value(2, modes)
        reg_c = self.get_register(3, modes)
        self.set_value(reg_c, 1 if val_a == val_b else 0)
        self.ip += 4

    def adjust_relative_base(self, modes):
        self.relative_base += self.get_value(1, modes)
        self.ip += 2

    def exit(self, modes):
        self.ip += 1
        self.running = False

    def get_value(self, index, modes):
        if index == 1:
            mode = (modes) % 10
        elif index == 2:
            mode = (modes // 10) % 10
        elif index == 3:
            mode = (modes // 100) % 10
        else:
            raise NotImplementedError()
        if mode == 0:
            return self.program[self.program[self.ip + index]]
        elif mode == 1:
            return self.program[self.ip + index]
        elif mode == 2:
            return self.program[self.program[self.ip + index] + self.relative_base]

    def get_register(self, index, modes):
        if index == 1:
            mode = (modes) % 10
        elif index == 2:
            mode = (modes // 10) % 10
        elif index == 3:
            mode = (modes // 100) % 10
        else:
            raise NotImplementedError("Index not implemented")
        val = self.program[self.ip + index]
        if mode == 0:
            return val
        elif mode == 2:
            return self.relative_base + val
        else:
            raise NotImplementedError("Mode not implemented")

    def set_value(self, index, val):
        self.program[index] = val

LF = 10

class ascii_computer:
    def __init__(self, program):
        self.intcode_computer = computer(program)
        self.output = self.intcode_computer.output

    def lines(self):
        while self.intcode_computer.running:
            yield self.read_line()

    def read_line(self):
        output = []
        byte = None
        while byte != LF and self.intcode_computer.running:
            byte = self.intcode_computer.run_until_output()
            if byte is not None and byte >= 0 and byte < 128:
                output.append(byte)
        if byte == LF:
            output.pop()
        return ''.join(map(chr, output))

    def write_line(self, line):
        for c in map(ord, line):
            self.intcode_computer.input.append(c)
        self.intcode_computer.input.append(LF)

    def run(self):
        self.intcode_computer.run()

    def run_interactive(self):
        for c in self.intcode_computer.iterator(self.get_input):
            if c == LF:
                print()
            else:
                print(chr(c), end = '')

    def get_input(self, computer):
        data = input('> ')
        self.write_line(data)
