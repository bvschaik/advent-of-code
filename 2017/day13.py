import adventofcode
import math

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(13)

    def reset(self):
        self.guards = []

    def input_line(self, line):
        (depth, size) = line.split(': ')
        self.guards.append((int(depth), int(size), (int(size) - 1) * 2))

    def solve1(self):
        severity = 0
        for depth, size, period in self.guards:
            if depth % period == 0:
                severity += depth * size
        return str(severity)

    def solve2(self):
        # Find the periods which have only 1 slot in which it's possible to pass through
        periods = self.get_periods_with_one_solution()

        # Combine these periods: they are guaranteed to have only 1 allowed solution in lcm(p1, p2)
        big_period = 1
        big_allowed = 0
        for p, p_allowed in periods.items():
            (big_period, big_allowed) = self.merge(big_period, big_allowed, p, p_allowed)

        # "Brute-force" solution by trying all multiples of the allowed number
        delay = -big_allowed
        delay_inc = big_period
        success = False
        while not success:
            delay += delay_inc
            success = True
            for depth, size, period in self.guards:
                if (depth + delay) % period == 0:
                    success = False
                    break
        return str(delay)

    def get_periods_with_one_solution(self):
        periods = dict()
        for depth, size, period in self.guards:
            if period not in periods:
                periods[period] = set()
            periods[period].add(depth % period)
        for p1 in periods:
            for p2 in periods:
                if p1 < p2 and p2 % p1 == 0:
                    for n in range(0, p2, p1):
                        for forbidden in periods[p1]:
                            periods[p2].add(forbidden + n)
        one_solution = dict()
        for p in periods:
            if len(periods[p]) == p - 1:
                p_allowed = (set(range(p)) - periods[p]).pop()
                one_solution[p] = p_allowed
        return one_solution

    def merge(self, p1, allowed1, p2, allowed2):
        lcm = (p1 * p2) // math.gcd(p1, p2)
        combined_allowed = []
        for n1 in range(0, lcm, p1):
            for n2 in range(0, lcm, p2):
                if allowed1 + n1 == allowed2 + n2:
                    combined_allowed.append(allowed1 + n1)
        return (lcm, combined_allowed[0])

    def solve2_brute_force(self):
        delay = 0
        success = False
        while not success:
            delay += 1
            success = True
            for depth, size, period in self.guards:
                if (depth + delay) % period == 0:
                    success = False
                    break
        return str(delay)

r = runner()

r.test('Sample', [
    '0: 3',
    '1: 2',
    '4: 4',
    '6: 4',
], '24', '10')

r.run()
