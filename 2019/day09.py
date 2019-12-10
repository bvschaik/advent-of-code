import adventofcode
from collections import defaultdict

class intcode_computer:
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
            opcode = self.program[self.ip] % 100
            self.opcodes[opcode]()
            if opcode == 4:
                return self.output[-1]
        return None

    def add(self, modes):
        # print("ADD %d (%d %d %d)" % (self.program[self.ip + 0], self.program[self.ip + 1], self.program[self.ip + 2], self.program[self.ip + 3]))
        val_a = self.get_value(1, modes)
        val_b = self.get_value(2, modes)
        reg_c = self.get_register(3, modes)
        self.set_value(reg_c, val_a + val_b)
        self.ip += 4

    def multiply(self, modes):
        # print("MUL %d (%d %d %d)" % (self.program[self.ip + 0], self.program[self.ip + 1], self.program[self.ip + 2], self.program[self.ip + 3]))
        val_a = self.get_value(1, modes)
        val_b = self.get_value(2, modes)
        reg_c = self.get_register(3, modes)
        self.set_value(reg_c, val_a * val_b)
        self.ip += 4

    def read_input(self, modes):
        # print("IN %d %d" % (self.program[self.ip + 0], self.program[self.ip + 1]))
        reg_a = self.get_register(1, modes)
        self.set_value(reg_a, self.input.pop(0))
        self.ip += 2

    def write_output(self, modes):
        val = self.get_value(1, modes)
        # print("OUT %d %d = %d" % (self.program[self.ip + 0], self.program[self.ip + 1], val))
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
        # print("REL += %d" % val_a)
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

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(9)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computer = intcode_computer(list(self.data), [1])
        computer.run()
        return str(computer.output[0])

    def solve2(self):
        computer = intcode_computer(list(self.data), [2])
        computer.run()
        return str(computer.output[0])

r = runner()

# r.test('Sample 1', ['109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'], 'x')
# r.test('Sample 3', ['104,1125899906842624,99'], '139629729')

r.run()
