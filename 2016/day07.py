import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(7)

    def reset(self):
        self.addresses = []

    def input_line(self, line):
        parts = line.split('[')
        non_hypernet = [parts.pop(0)]
        hypernet = []
        for p in parts:
            split = p.split(']')
            hypernet.append(split[0])
            non_hypernet.append(split[1])
        self.addresses.append((non_hypernet, hypernet))

    def solve1(self):
        with_tls = 0
        for non_hypernet, hypernet in self.addresses:
            if any(map(lambda x: self.has_abba(x), non_hypernet)) and not any(map(lambda x: self.has_abba(x), hypernet)):
                with_tls += 1
        return str(with_tls)

    def has_abba(self, value):
        for n in range(len(value) - 3):
            if value[n] == value[n+3] and value[n+1] == value[n+2] and value[n] != value[n+1]:
                return True
        return False

    def solve2(self):
        with_ssl = 0
        for non_hypernet, hypernet in self.addresses:
            for bab in self.find_aba_as_bab(non_hypernet):
                if self.contains_bab(hypernet, bab):
                    with_ssl += 1
                    break
        return str(with_ssl)

    def find_aba_as_bab(self, values):
        babs = []
        for value in values:
            for n in range(len(value) - 2):
                if value[n] == value[n+2] and value[n] != value[n+1]:
                    yield value[n+1] + value[n] + value[n+1]

    def contains_bab(self, values, bab):
        for v in values:
            if v.find(bab) >= 0:
                return True
        return False

r = runner()
r.run()
