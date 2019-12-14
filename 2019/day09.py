import adventofcode
import intcode
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(9)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computer = intcode.computer(list(self.data), [1])
        computer.run()
        return str(computer.output[0])

    def solve2(self):
        computer = intcode.computer(list(self.data), [2])
        computer.run()
        return str(computer.output[0])

r = runner()

# r.test('Sample 1', ['109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'], 'x')
# r.test('Sample 3', ['104,1125899906842624,99'], '139629729')

r.run()
