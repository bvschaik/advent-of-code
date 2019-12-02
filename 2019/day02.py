import adventofcode

class intcode_computer:
    def __init__(self, program):
        self.program = program
        self.ip = 0

    def run(self):
        while True:
            opcode = self.program[self.ip]
            if opcode == 99:
                return
            elif opcode == 1:
                self.add()
            elif opcode == 2:
                self.multiply()

    def add(self):
        reg_a = self.program[self.ip + 1]
        reg_b = self.program[self.ip + 2]
        reg_c = self.program[self.ip + 3]
        self.program[reg_c] = self.program[reg_a] + self.program[reg_b]
        self.ip += 4

    def multiply(self):
        reg_a = self.program[self.ip + 1]
        reg_b = self.program[self.ip + 2]
        reg_c = self.program[self.ip + 3]
        self.program[reg_c] = self.program[reg_a] * self.program[reg_b]
        self.ip += 4

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(2)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        program = list(self.data)
        program[1] = 12
        program[2] = 2
        computer = intcode_computer(program)
        computer.run()
        return str(computer.program[0])

    def solve2(self):
        target = 19690720

        # Since the computer can only add and multiply, the value can only increase.
        # So increasing start values give increasing results.

        # Check whether noun or verb is the major factor
        if self.run_computer_with(100, 0) >= target:
            # Noun is the major factor
            min_noun = 0
            for noun in range(100):
                if self.run_computer_with(noun, 0) > target:
                    min_noun = noun - 1
                    break

            for noun in range(min_noun, 100):
                for verb in range(100):
                    if self.run_computer_with(noun, verb) == target:
                        return str(100 * noun + verb)

        elif self.run_computer_with(0, 100) >= target:
            # Verb is the major factor
            min_verb = 0
            for verb in range(100):
                if self.run_computer_with(0, verb) > target:
                    min_verb = verb - 1
                    break

            for verb in range(min_verb, 100):
                for noun in range(100):
                    if self.run_computer_with(noun, verb) == target:
                        return str(100 * noun + verb)

        else:
            # A combination of both is the major factor... just try them all
            for noun in range(100):
                for verb in range(100):
                    if self.run_computer_with(noun, verb) == target:
                        return str(100 * noun + verb)

    def run_computer_with(self, noun, verb):
        program = list(self.data)
        program[1] = noun
        program[2] = verb
        computer = intcode_computer(program)
        computer.run()
        return computer.program[0]

r = runner()

r.run()
