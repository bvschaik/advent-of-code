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
        freqs = set()
        while freq not in freqs:
            for i in self.inputs:
                freqs.add(freq)
                freq += i
                if freq in freqs:
                    return str(freq)
            print("Iterating again")
        raise AssertionError("Should not happen")

day01().solve()
