from runner import runner

class day02(runner):
    inputs = []

    def day(self):
        return 2
    
    def input(self, line):
        self.inputs.append(line)

    def solve1(self):
        two_letters = 0
        three_letters = 0
        for code in self.inputs:
            letters = dict()
            for letter in code:
                if letter in letters:
                    letters[letter] += 1
                else:
                    letters[letter] = 1
            two = False
            three = False
            for letter, frequency in letters.items():
                if frequency == 2:
                    two = True
                elif frequency == 3:
                    three = True
            if two:
                two_letters += 1
            if three:
                three_letters += 1
        return str(two_letters * three_letters)

    def solve2(self):
        # Assumption: barcodes are all the same length
        codelen = len(self.inputs[0])
        for index in range(codelen):
            values = set()
            for code in self.inputs:
                newcode = code[:index] + code[index+1:]
                if newcode in values:
                    return newcode
                values.add(newcode)

        raise AssertionError("Should not happen")

day02().solve()
