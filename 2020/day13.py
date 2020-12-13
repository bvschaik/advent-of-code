import adventofcode
import math

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(13)

    def reset(self):
        self.timestamp = 0
        self.buses = []

    def input_line(self, line):
        if self.timestamp:
            self.buses = line.split(',')
        else:
            self.timestamp = int(line)

    def solve1(self):
        buses = list(map(int, filter(lambda b: b != 'x', self.buses)))
        bus = min(map(lambda b: (b, b - self.timestamp % b), buses), key = lambda b: b[1])
        return str(bus[0] * bus[1])

    def solve2(self):
        buses = list(map(lambda b: (b[0], int(b[1])), filter(lambda b: b[1] != 'x', enumerate(self.buses))))
        lcm = 1
        remainder = 0
        for offset, bus in buses:
            remainder = self.find_remainder(lcm, remainder, bus, (bus - offset) % bus)
            # All input numbers are prime, so they are also co-prime. LCM = simple multiplication
            lcm = lcm * bus
            # print(lcm)
        return str(remainder)

    def find_remainder(self, n1, a1, n2, a2):
        # Chinese remainder theorem using a simple sieve:
        # Z === a1 (mod n1)
        # Z === a2 (mod n2)
        # We need to find the solution to the equation:
        # x * n1 + a1 == y * n2 + a2
        # Or alternatively without y:
        # (x * n1 + a1) % n2 == a2
        # We iterate X and check whether it fits the bill
        # Then return the "remainder" for the multiple
        # In our case, n1,n2 = bus1/bus2 id, a1,a2 = time offset for buses
        for x in range(0, n2 + 1):
            multiple = x * n1 + a1
            if multiple % n2 == a2:
                return multiple

r = runner()

r.test('Sample 1', [
    '939',
    '7,13,x,x,59,x,31,19',
], '295', '1068781')

r.run()
