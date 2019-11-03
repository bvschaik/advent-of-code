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
        for id in self.inputs:
            letters = dict()
            for letter in id:
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
        max = len(self.inputs)
        for i in range(max):
            a = self.inputs[i]
            for j in range(i + 1, max):
                b = self.inputs[j]
                if (self.almost_equal(a, b)):
                    return self.common_part(a, b)

    def common_part(self, a, b):
        result = ""
        length = len(a)
        for i in range(length):
            if a[i] == b[i]:
                result += str(a[i])
        return result

    def almost_equal(self, a, b):
        length = len(a)
        has_mistake = False
        for i in range(length):
            if a[i] != b[i]:
                if has_mistake:
                    return False
                has_mistake = True
        return has_mistake

day02().solve()
