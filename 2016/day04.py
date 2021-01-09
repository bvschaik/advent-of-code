import adventofcode
import re
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(4)

    def reset(self):
        self.rooms = []

    def input_line(self, line):
        m = re.match(r'([a-z-]*)-(\d+)\[([a-z]*)\]', line)
        self.rooms.append((m.group(1), int(m.group(2)), m.group(3)))

    def solve1(self):
        self.valid_rooms = []
        total = 0
        for (name, sector, checksum) in self.rooms:
            if self.is_valid(name, checksum):
                total += sector
                self.valid_rooms.append((name, sector))
        return str(total)

    def is_valid(self, name, checksum):
        letters = defaultdict(int)
        for c in name.replace('-', ''):
            letters[c] += 1
        sorted_letters = sorted(letters.items(), key = lambda x: (-x[1], x[0]))[0:5]
        most_frequent = map(lambda x: x[0], sorted_letters)
        return ''.join(most_frequent) == checksum

    def solve2(self):
        for (name, sector) in self.valid_rooms:
            real_name = self.decrypt(name, sector)
            if real_name.find('northpole') >= 0:
                return str(sector)

    def decrypt(self, name, sector):
        offset = sector % 26
        a_id = ord('a')
        decrypted = ''
        for c in name:
            if c == '-':
                letter = ' '
            else:
                letter = chr(a_id + ((ord(c) - a_id) + sector) % 26)
            decrypted += letter
        return decrypted

r = runner()

r.test('Sample', [
    'aaaaa-bbb-z-y-x-123[abxyz]',
    'a-b-c-d-e-f-g-h-987[abcde]',
    'not-a-real-room-404[oarel]',
    'totally-real-room-200[decoy]',
], '1514')

r.run()
