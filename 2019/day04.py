import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(4)

    def reset(self):
        self.start = 0
        self.end = 0

    def input_line(self, line):
        (self.start, self.end) = map(int, line.split('-'))

    def solve1(self):
        result = []
        for i in range(1, 10):
            self.generate_passwords(i, 1, False, result)
        return str(len(result))

    def generate_passwords(self, number, index, has_dupe, result):
        if index == 6:
            if has_dupe:
                if number >= self.start and number <= self.end:
                    result.append(number)
            return

        last = number % 10
        self.generate_passwords(number * 10 + last, index + 1, True, result)
        for i in range(last + 1, 10):
            self.generate_passwords(number * 10 + i, index + 1, has_dupe, result)

    def solve2(self):
        result = []
        for i in range(1, 10):
            self.generate_passwords2(i, 1, False, 1, result)
        return str(len(result))

    def generate_passwords2(self, number, index, has_dupe, dupe_count, result):
        if index == 6:
            if has_dupe or dupe_count == 2:
                if number >= self.start and number <= self.end:
                    result.append(number)
            return

        last = number % 10
        self.generate_passwords2(number * 10 + last, index + 1, has_dupe, dupe_count + 1, result)
        for i in range(last + 1, 10):
            self.generate_passwords2(number * 10 + i, index + 1, has_dupe or dupe_count == 2, 1, result)

r = runner()

r.run()
