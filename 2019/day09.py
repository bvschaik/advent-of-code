import adventofcode

class intcode_computer:
    def __init__(self, program, input = []):
        self.program = program
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
            opcode = self.program[self.ip] % 100
            self.opcodes[opcode]()

    def run_until_output(self):
        while self.running:
            opcode = self.program[self.ip] % 100
            self.opcodes[opcode]()
            if opcode == 4:
                return self.output[-1]
        return None

    def add(self):
        # print("ADD %d (%d %d %d)" % (self.program[self.ip + 0], self.program[self.ip + 1], self.program[self.ip + 2], self.program[self.ip + 3]))
        val_a = self.get_value(1)
        val_b = self.get_value(2)
        reg_c = self.get_register(3)
        self.set_value(reg_c, val_a + val_b)
        self.ip += 4

    def multiply(self):
        # print("MUL %d (%d %d %d)" % (self.program[self.ip + 0], self.program[self.ip + 1], self.program[self.ip + 2], self.program[self.ip + 3]))
        val_a = self.get_value(1)
        val_b = self.get_value(2)
        reg_c = self.get_register(3)
        self.set_value(reg_c, val_a * val_b)
        self.ip += 4

    def read_input(self):
        # print("IN %d %d" % (self.program[self.ip + 0], self.program[self.ip + 1]))
        reg_a = self.get_register(1)
        self.set_value(reg_a, self.input.pop(0))
        self.ip += 2

    def write_output(self):
        val = self.get_value(1)
        # print("OUT %d %d = %d" % (self.program[self.ip + 0], self.program[self.ip + 1], val))
        self.output.append(val)
        self.ip += 2

    def jump_if_true(self):
        val = self.get_value(1)
        if val:
            self.ip = self.get_value(2)
        else:
            self.ip += 3

    def jump_if_false(self):
        val = self.get_value(1)
        if val == 0:
            self.ip = self.get_value(2)
        else:
            self.ip += 3

    def less_than(self):
        val_a = self.get_value(1)
        val_b = self.get_value(2)
        reg_c = self.get_register(3)
        self.set_value(reg_c, 1 if val_a < val_b else 0)
        self.ip += 4

    def equals(self):
        val_a = self.get_value(1)
        val_b = self.get_value(2)
        reg_c = self.get_register(3)
        self.set_value(reg_c, 1 if val_a == val_b else 0)
        self.ip += 4

    def adjust_relative_base(self):
        val_a = self.get_value(1)
        # print("REL += %d" % val_a)
        self.relative_base += val_a
        self.ip += 2

    def exit(self):
        self.ip += 1
        self.running = False

    def get_value(self, index):
        if index == 1:
            mode = (self.program[self.ip] // 100) % 10
        elif index == 2:
            mode = (self.program[self.ip] // 1000) % 10
        elif index == 3:
            mode = (self.program[self.ip] // 10000) % 10
        else:
            raise NotImplementedError()
        val = self.program[self.ip + index]
        if mode == 0:
            val = self.program[val] if val < len(self.program) else 0
        elif mode == 2:
            val = self.program[val + self.relative_base]
        return val

    def get_register(self, index):
        if index == 1:
            mode = (self.program[self.ip] // 100) % 10
        elif index == 2:
            mode = (self.program[self.ip] // 1000) % 10
        elif index == 3:
            mode = (self.program[self.ip] // 10000) % 10
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
        self.expand_to_index(index)
        self.program[index] = val

    def expand_to_index(self, index):
        while index >= len(self.program):
            self.program.append(0)

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
