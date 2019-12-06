import adventofcode

class intcode_computer:
    def __init__(self, program, input = []):
        self.program = program
        self.ip = 0
        self.running = True
        self.input = input
        self.output = []
        self.opcodes = {
            1: self.add,
            2: self.multiply,
            3: self.read_input,
            4: self.write_output,
            99: self.exit
        }

    def run(self):
        while self.running:
            opcode = self.program[self.ip] % 100
            self.opcodes[opcode]()

    def add(self):
        print("ADD %d (%d %d %d)" % (self.program[self.ip + 0], self.program[self.ip + 1], self.program[self.ip + 2], self.program[self.ip + 3]))
        val_a = self.get_value(1)
        val_b = self.get_value(2)
        reg_c = self.program[self.ip + 3]
        self.program[reg_c] = val_a + val_b
        self.ip += 4

    def multiply(self):
        print("MUL %d (%d %d %d)" % (self.program[self.ip + 0], self.program[self.ip + 1], self.program[self.ip + 2], self.program[self.ip + 3]))
        val_a = self.get_value(1)
        val_b = self.get_value(2)
        reg_c = self.program[self.ip + 3]
        self.program[reg_c] = val_a * val_b
        self.ip += 4

    def read_input(self):
        print("IN %d %d" % (self.program[self.ip + 0], self.program[self.ip + 1]))
        reg_a = self.program[self.ip + 1]
        self.program[reg_a] = self.input[0]
        del self.input[0]
        self.ip += 2

    def write_output(self):
        print("OUT %d %d" % (self.program[self.ip + 0], self.program[self.ip + 1]))
        val = self.get_value(1)
        self.output.append(val)
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
            val = self.program[val]
        return val

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(5)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computer = intcode_computer(list(self.data), [1])
        computer.run()
        print(computer.output)
        return computer.output[-1]

    def solve2(self):
        pass

r = runner()

r.run()
