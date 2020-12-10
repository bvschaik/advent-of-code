import adventofcode
from collections import deque
from collections import defaultdict

class xmas:
    def __init__(self, initial_numbers):
        self.valid = defaultdict(int)
        self.numbers = deque()
        for i in initial_numbers:
            self.add(i)

    def process(self, number):
        if self.is_valid(number):
            self.remove_first()
            self.add(number)
            return True
        else:
            return False

    def add(self, number):
        for n in self.numbers:
            if number != n:
                self.valid[number + n] += 1
        self.numbers.append(number)

    def remove_first(self):
        number = self.numbers.popleft()
        for n in self.numbers:
            if number != n:
                self.valid[number + n] -= 1

    def is_valid(self, number):
        return self.valid[number] > 0

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(9)

    def reset(self):
        self.numbers = []
        self.invalid_number = 0
        self.invalid_index = 0

    def input_line(self, line):
        self.numbers.append(int(line))

    def solve1(self):
        x = xmas(self.numbers[0:25])
        for i in range(25, len(self.numbers)):
            number = self.numbers[i]
            if not x.process(number):
                self.invalid_number = number
                self.invalid_index = i
                return str(number)

    def solve2(self):
        all_numbers = self.numbers[0:self.invalid_index]
        target = self.invalid_number
        start = 0
        end = 0
        total = 0
        while True:
            if total == target:
                subset = all_numbers[start:end]
                min_value = min(subset)
                max_value = max(subset)
                return str(min_value + max_value)
            if total < target:
                total += all_numbers[end]
                end += 1
            elif total > target:
                total -= all_numbers[start]
                start += 1

r = runner()

r.run()
