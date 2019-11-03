from runner import runner

class day01(runner):
    inputs = []

    def day(self):
        return 1
    
    def input(self, line):
        self.inputs.append(int(line))

    def solve1(self):
        freq = 0
        for i in self.inputs:
            freq += i
        return str(freq)

    def solve2(self):
        freq = 0
        lookup = set()
        freqs = list()
        for i in self.inputs:
            lookup.add(freq)
            freqs.append(freq)
            freq += i
            if freq in lookup:
                return str(freq)

        multiplier = 1
        while True:
            offset = freq * multiplier
            for f in freqs:
                if (offset + f) in lookup:
                    return str(offset + f)
            multiplier += 1

        raise AssertionError("Should not happen")

day01().solve()
