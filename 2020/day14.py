import adventofcode
import re

TYPE_MASK = 1
TYPE_MEM = 2

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(14)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        if line.startswith('mask'):
            self.instructions.append((TYPE_MASK, line[7:]))
        else:
            m = re.match(r'mem\[(\d+)\] = (\d+)', line)
            self.instructions.append((TYPE_MEM, int(m.group(1)), int(m.group(2))))

    def solve1(self):
        mask_and = 0xfffffffff
        mask_or = 0
        memory = dict()
        for instr in self.instructions:
            if instr[0] == TYPE_MASK:
                mask_and = 0
                mask_or = 0
                for c in instr[1]:
                    mask_and <<= 1
                    mask_or <<= 1
                    if c == '1':
                        mask_or |= 1
                    if c != '0':
                        mask_and |= 1
            else:
                offset = instr[1]
                value = instr[2]
                memory[offset] = (value & mask_and) | mask_or
        return str(sum(memory.values()))

    def solve2(self):
        mask_and = 0xfffffffff
        mask_or = 0
        floaties = []
        memory = dict()
        for instr in self.instructions:
            if instr[0] == TYPE_MASK:
                mask_and = 0
                mask_or = 0
                floaties = [0]
                for index, c in enumerate(reversed(instr[1])):
                    value = 1 << index
                    if c == '1':
                        mask_or |= value
                    if c != 'X':
                        mask_and |= value
                    if c == 'X':
                        length = len(floaties)
                        for i in range(length):
                            floaties.append(floaties[i] + value)
            else:
                offset = (instr[1] & mask_and) | mask_or
                value = instr[2]
                for index in floaties:
                    memory[offset + index] = value
        return str(sum(memory.values()))

r = runner()

r.test('Sample 1', [
    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    'mem[8] = 11',
    'mem[7] = 101',
    'mem[8] = 0',
], '165')

r.test('Sample 2', [
    'mask = 000000000000000000000000000000X1001X',
    'mem[42] = 100',
    'mask = 00000000000000000000000000000000X0XX',
    'mem[26] = 1',
], None, '208')

r.run()
