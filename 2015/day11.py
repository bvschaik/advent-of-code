import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(11)

    def reset(self):
        self.password = None

    def input_line(self, line):
        self.password = line

    def solve1(self):
        password = list(self.password)
        self.increment(password)
        while not self.is_valid(password):
            self.increment(password)
        self.new_password = ''.join(password)
        return self.new_password

    def solve2(self):
        password = list(self.new_password)
        self.increment(password)
        while not self.is_valid(password):
            self.increment(password)
        return ''.join(password)

    def increment(self, password):
        index = 7
        while True:
            c = password[index]
            if c == 'z':
                password[index] = 'a'
                index -= 1
            elif c == 'h' or c == 'k' or c == 'n':
                password[index] = chr(ord(password[index]) + 2)
                break
            else:
                password[index] = chr(ord(password[index]) + 1)
                break

    def is_valid(self, password):
        if 'i' in password or 'o' in password or 'l' in password:
            return False
        # Check for pairs
        prev = None
        pairs = set()
        for c in password:
            if c == prev:
                pairs.add(c)
            prev = c
        if len(pairs) < 2:
            return False
        # Check for increasing sequence
        prev = 0
        seq_len = 0
        max_seq = 0
        for c in password:
            if prev + 1 == ord(c):
                seq_len += 1
            else:
                if seq_len > max_seq:
                    max_seq = seq_len
                seq_len = 1
            prev = ord(c)
        if max_seq < 3:
            return False
        return True

r = runner()

r.test('Sample', [
    'abcdefgh',
], 'abcdffaa')

r.run()
