import adventofcode
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(1)

    def reset(self):
        self.inputs = []

    def input_line(self, line):
        self.inputs.append(int(line))

    def solve1(self):
        freq = 0
        for i in self.inputs:
            freq += i
        return str(freq)

    def solve2(self):
        freqs = list()
        freq = 0
        for i in self.inputs:
            freqs.append(freq)
            freq += i

        modulo = freq
        if modulo == 0:
            # Edge case: modulo is 0: solution is either a repeating number in the list or 0
            seen = set()
            for f in freqs:
                if f in seen:
                    return str(f)
                seen.add(f)
            return str(0)

        # Every further iteration of the input list will return in 'freqs' offset by 'modulo'.
        # So now, we need to find a number 'x' in the list, for which this formula holds:
        # x + modulo * repeats = y, where y is another number in the list, and repeats is minimized.
        # We know that both x and y should have the same remainder when divided by 'modulo',
        # so prepare a dictionary for efficiency.
        remainders = defaultdict(list)
        for f in freqs:
            rem = f % modulo
            if f in remainders[rem]:
                # Edge case: first iteration contains duplicate number
                return str(f)
            remainders[rem].append(f)
        
        min = modulo + 1
        min_value = -1
        for source in freqs:
            for target in remainders[source % modulo]:
                if source != target:
                    repeats = (target - source) / modulo
                    if repeats >= 0 and repeats < min:
                        min = repeats
                        min_value = target
        return str(min_value)

r = runner()

r.test('Zero frequency', ['1', '-1'], '0', '0')
r.test('Zero frequency with same freq in initial set', ['1', '1', '-1', '-1'], '0', '1')
r.test('Same frequency within initial set', ['1', '1', '-1'], '1', '1')

r.run()
