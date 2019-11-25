import adventofcode
import hashlib

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(4)

    def reset(self):
        self.key = ''

    def input_line(self, line):
        self.key = line

    def solve1(self):
        base = hashlib.md5()
        base.update(self.key.encode('utf-8'))

        number = 1
        while True:
            copy = base.copy()
            copy.update(str(number).encode('utf-8'))
            if copy.hexdigest().startswith('00000'):
                return str(number)
            number += 1

    def solve2(self):
        base = hashlib.md5()
        base.update(self.key.encode('utf-8'))

        number = 1
        while True:
            copy = base.copy()
            copy.update(str(number).encode('utf-8'))
            if copy.hexdigest().startswith('000000'):
                return str(number)
            number += 1

r = runner()

r.test('Sample 1', ['abcdef'], '609043')
r.test('Sample 2', ['pqrstuv'], '1048970')

r.run()
