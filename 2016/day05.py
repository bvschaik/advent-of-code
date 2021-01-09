import adventofcode
import hashlib

HEXCHARS = '0123456789abcdef'

def five_zero_hashes(door_id):
    index = 0
    while True:
        key = door_id + str(index)
        digest = hashlib.md5(key.encode('utf-8')).digest()
        if digest[0] == 0 and digest[1] == 0 and digest[2] < 16:
            yield digest
        index += 1

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(5)

    def reset(self):
        self.door_id = None

    def input_line(self, line):
        self.door_id = line

    def solve1(self):
        self.hashes = []
        self.last_index = 0
        password = ''
        index = 0
        hasher = five_zero_hashes(self.door_id)
        for digest in hasher:
            password += HEXCHARS[digest[2]]
            print(password)
            if len(password) == 8:
                break
        return password

    def solve2(self):
        password = ['_'] * 8
        found = 0
        hasher = five_zero_hashes(self.door_id)
        for digest in hasher:
            position = digest[2]
            if position < 8 and password[position] == '_':
                password[position] = HEXCHARS[digest[3] >> 4]
                print(''.join(password))
                found += 1
                if found == 8:
                    break
        return ''.join(password)

r = runner()
r.run()
