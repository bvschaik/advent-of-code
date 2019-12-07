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
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
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
        reg_c = self.program[self.ip + 3]
        self.program[reg_c] = val_a + val_b
        self.ip += 4

    def multiply(self):
        # print("MUL %d (%d %d %d)" % (self.program[self.ip + 0], self.program[self.ip + 1], self.program[self.ip + 2], self.program[self.ip + 3]))
        val_a = self.get_value(1)
        val_b = self.get_value(2)
        reg_c = self.program[self.ip + 3]
        self.program[reg_c] = val_a * val_b
        self.ip += 4

    def read_input(self):
        # print("IN %d %d" % (self.program[self.ip + 0], self.program[self.ip + 1]))
        reg_a = self.program[self.ip + 1]
        self.program[reg_a] = self.input[0]
        del self.input[0]
        self.ip += 2

    def write_output(self):
        # print("OUT %d %d" % (self.program[self.ip + 0], self.program[self.ip + 1]))
        val = self.get_value(1)
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
        reg_c = self.program[self.ip + 3]
        self.program[reg_c] = 1 if val_a < val_b else 0
        self.ip += 4

    def equals(self):
        val_a = self.get_value(1)
        val_b = self.get_value(2)
        reg_c = self.program[self.ip + 3]
        self.program[reg_c] = 1 if val_a == val_b else 0
        self.ip += 4

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
        super().__init__(7)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        return str(self.permute_and_run({0, 1, 2, 3, 4}, 0))

    def permute_and_run(self, phases, input):
        if len(phases) == 1:
            for p in phases:
                return self.run_computer(p, input)
        max_result = 0
        for p in phases:
            new_phases = phases - {p}
            new_input = self.run_computer(p, input)
            result = self.permute_and_run(new_phases, new_input)
            if result > max_result:
                max_result = result
        return max_result

    def run_computer(self, phase, input):
        computer = intcode_computer(list(self.data), [phase, input])
        computer.run()
        return computer.output[-1]

    def solve2(self):
        return str(self.permute_and_run_feedback({5, 6, 7, 8, 9}))

    def permute_and_run_feedback(self, phases_left, phases_chosen = []):
        if not phases_left:
            return self.run_feedback(phases_chosen)
        max_result = 0
        for p in phases_left:
            new_phases = phases_left - {p}
            phases_chosen.append(p)
            result = self.permute_and_run_feedback(new_phases, phases_chosen)
            phases_chosen.pop()
            if result > max_result:
                max_result = result
        return max_result

    def run_feedback(self, phases):
        computers = []
        for p in phases:
            computers.append(intcode_computer(list(self.data), [p]))
        input = 0
        halted = False
        while not halted:
            for c in computers:
                c.input.append(input)
                input = c.run_until_output()
                if input == None:
                    halted = True
                    break
        return computers[-1].output[-1]

r = runner()

r.test('Sample 1', ['3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'], '43210')
r.test('Sample 2.1', ['3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'], None, '139629729')

r.run()
