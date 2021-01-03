import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(8)

    def reset(self):
        self.lines = []

    def input_line(self, line):
        self.lines.append(line)

    def solve1(self):
        string_chars = 0
        memory_chars = 0
        for line in self.lines:
            string_chars += len(line)
            memory_chars += self.decode_length(line)
        return str(string_chars - memory_chars)

    def decode_length(self, line):
        length = 0
        escape = False
        hexchar = 0
        for c in line[1:-1]:
            if escape:
                escape = False
                if c == 'x':
                    hexchar = 2
                    length += 1
                elif c == '"' or c == '\\':
                    length += 1
                else:
                    print("Invalid string")
            elif hexchar > 0:
                hexchar -= 1
            elif c == '\\':
                escape = True
            else:
                length += 1
        return length

    def solve2(self):
        string_chars = 0
        memory_chars = 0
        for line in self.lines:
            memory_chars += len(line)
            string_chars += self.encode_length(line)
        return str(string_chars - memory_chars)

    def encode_length(self, line):
        length = 2 # quotes at start and end
        for c in line:
            if c == '\\' or c == '"':
                length += 2
            else:
                length += 1
        return length

r = runner()

r.test('Sample', [
    '""',
    '"abc"',
    '"aaa\\"aaa"',
    '"\\x27"',
], '12', '19')

r.run()
