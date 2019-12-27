import adventofcode
import intcode

NOT = 'NOT'
AND = 'AND'
OR = 'OR'
REG_J = 0
REGISTERS = 'JTABCDEFGHI'

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6
H = 7
I = 8

class springscript:
    def __init__(self):
        self.instructions = []

    def write_line(self, line):
        i, a, b = line.split(' ')
        self.instructions.append((i, REGISTERS.index(a), REGISTERS.index(b)))

    def walk(self, a, b, c, d):
        registers = [False, False, a, b, c, d]
        for i, r1, r2 in self.instructions:
            if i == NOT:
                registers[r2] = not registers[r1]
            elif i == AND:
                registers[r2] = registers[r1] and registers[r2]
            elif i == OR:
                registers[r2] = registers[r1] or registers[r2]
        return registers[REG_J]

    def run(self, config, debug = False):
        if debug:
            print(config)
        registers = [False, False]
        for c in config:
            registers.append(True if c == '#' else False)
        for i, r1, r2 in self.instructions:
            if i == NOT:
                registers[r2] = not registers[r1]
            elif i == AND:
                registers[r2] = registers[r1] and registers[r2]
            elif i == OR:
                registers[r2] = registers[r1] or registers[r2]
            if debug:
                print(i.ljust(3), REGISTERS[r1], REGISTERS[r2], registers)
        return registers[REG_J]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(21)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computer = intcode.ascii_computer(self.data)
        print(computer.read_line())

        self.enter_program1(computer)

        computer.write_line('WALK')

        for line in computer.lines():
            print(line)

        return str(computer.output[-1])

    def enter_program1(self, computer):
        # Formula:
        # not A or ((not B or not C) and D)
        computer.write_line('NOT B J')
        computer.write_line('NOT C T')
        computer.write_line('OR T J')
        computer.write_line('AND D J')
        computer.write_line('NOT A T')
        computer.write_line('OR T J')

    def try1(self):
        computer = springscript()

        for a in [True, False]:
            for b in [True, False]:
                for c in [True, False]:
                    for d in [True, False]:
                        result = computer.walk(a, b, c, d)
                        print('#' if a else '.', end = '')
                        print('#' if b else '.', end = '')
                        print('#' if c else '.', end = '')
                        print('#' if d else '.', end = '')
                        print('  jump' if result else '  walk')

    def solve2(self):
        computer = intcode.ascii_computer(self.data)
        print(computer.read_line())

        self.enter_program2(computer)

        computer.write_line('RUN')

        for line in computer.lines():
            print(line)

        return str(computer.output[-1])

    def enter_program2(self, computer):
        # Total formula:
        # (not A) or (A and ((not B) or (not C)) and D and (E or H)):

        # (not B) or (not C) --> J
        computer.write_line('NOT B J')
        computer.write_line('NOT C T')
        computer.write_line('OR T J')

        # Need to clear T before use...
        computer.write_line('NOT J T')
        computer.write_line('AND J T')
        # D and (E or H)) --> T
        computer.write_line('OR E T')
        computer.write_line('OR H T')
        computer.write_line('AND D T')

        # ((not B) or (not C)) and D and (E or H) --> J
        computer.write_line('AND T J')

        # A and ((not B) or (not C)) and D and (E or H) --> J
        computer.write_line('AND A J')

        # not A or ... -> J
        computer.write_line('NOT A T')
        computer.write_line('OR T J')

    def try2(self):
        computer = springscript()

        self.enter_program2(computer)

        for x in range(512):
            config = '{0:b}'.format(x).zfill(9).replace('0', '.').replace('1', '#')
            if not self.is_possible(config):
                continue
            jump = False
            # if config[A] == '.' or (config[A] == '#' and (config[B] == '.' or config[C] == '.') and config[D] == '#' and (config[E] == '#' or config[H] == '#')):
            if config[A] != '#' or (config[A] == '#' and (config[B] != '#' or config[C] != '#') and config[D] == '#' and (config[E] == '#' or config[H] == '#')):
                print(config, 'jump')
                jump = True
                pass
            else:
                print(config, 'walk')
                pass
            if computer.run(config) != jump:
                print(config, 'oops', jump)
                pass

    def is_possible(self, config):
        # Cannot jump a 4-wide hole
        if config.find('....') >= 0:
            return False
        # We have to jump but no ground to jump to
        if config[0] == '.' and config[3] == '.':
            return False
        # We have to jump and then jump again but no ground to jump to
        if config[0] == '.' and config[3] == '#' and config[4] == '.' and config[7] == '.':
            return False
        # Same as above but walk first
        if config[0] == '#' and config[1] == '.' and config[4] == '#' and config[5] == '.' and config[8] == '.':
            return False
        # Pattern #.?#.??. --> if we jump we get stuck, if we walk then jump we get stuck
        if config[0] == '#' and config[1] == '.' and config[3] == '#' and config[4] == '.' and config[7] == '.':
            return False
        return True

r = runner()

# r.try1()
# r.try2()

r.run()
