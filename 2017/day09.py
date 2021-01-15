import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(9)

    def reset(self):
        self.stream = None

    def input_line(self, line):
        self.stream = line

    def solve1(self):
        self.total_value = 0
        self.total_garbage = 0
        self.parse_group(0, 1)
        return str(self.total_value)

    def parse_group(self, i, depth):
        if self.stream[i] != '{':
            return None
        self.total_value += depth
        i += 1
        while self.stream[i] != '}':
            if self.stream[i] == '{':
                i = self.parse_group(i, depth + 1)
            elif self.stream[i] == '<':
                i = self.parse_garbage(i)
            else:
                i += 1
        return i + 1

    def parse_garbage(self, i):
        if self.stream[i] != '<':
            return 0
        i += 1
        while self.stream[i] != '>':
            if self.stream[i] == '!':
                i += 2
            else:
                self.total_garbage += 1
                i += 1
        return i + 1

    def solve2(self):
        return str(self.total_garbage)

r = runner()

r.test('Sample 1', ['{}'], '1')
r.test('Sample 2', ['{{{}}}'], '6')
r.test('Sample 3', ['{{},{}}'], '5')
r.test('Sample 4', ['{{{},{},{{}}}}'], '16')
r.test('Sample 5', ['{<a>,<a>,<a>,<a>}'], '1')
r.test('Sample 6', ['{{<ab>},{<ab>},{<ab>},{<ab>}}'], '9')
r.test('Sample 7', ['{{<!!>},{<!!>},{<!!>},{<!!>}}'], '9')
r.test('Sample 8', ['{{<a!>},{<a!>},{<a!>},{<ab>}}'], '3')

r.run()
