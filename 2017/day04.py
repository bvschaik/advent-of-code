import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(4)

    def reset(self):
        self.passphrases = []

    def input_line(self, line):
        self.passphrases.append(line.split())

    def solve1(self):
        valid = 0
        for phrase in self.passphrases:
            if len(set(phrase)) == len(phrase):
                valid += 1
        return str(valid)

    def solve2(self):
        valid = 0
        for phrase in self.passphrases:
            anagrams = set()
            for word in phrase:
                anagrams.add(''.join(sorted(word)))
            if len(anagrams) == len(phrase):
                valid += 1
        return str(valid)

r = runner()
r.run()
