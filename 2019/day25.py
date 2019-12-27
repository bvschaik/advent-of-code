import adventofcode
import intcode
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(25)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def play(self):
        computer = intcode.ascii_computer(self.data)
        computer.run_interactive()

    def solve1(self):
        commands = """
west
take mug
east
east
take coin
north
north
take hypercube
south
south
south
west
take astrolabe
north
east
north
east
""".splitlines()
        computer = intcode.ascii_computer(self.data)
        for cmd in commands:
            computer.write_line(cmd)

        for line in computer.lines():
            if 'get in by typing' in line:
                return re.match(r'.* (\d+) .*', line).group(1)

r = runner()

r.run()

