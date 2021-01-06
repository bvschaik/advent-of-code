import adventofcode
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(25)

    def reset(self):
        self.row = 0
        self.column = 0

    def input_line(self, line):
        m = re.match(r'.*Enter the code at row (\d+), column (\d+).', line)
        self.row = int(m.group(1))
        self.column = int(m.group(2))

    def solve1(self):
        # Values in row 1 are the sum of 1, 1-2, 1-3, etc = n * (n+1) / 2
        # Find the column id at row 1 on diagonal of the target
        first_row_column_id = self.row + self.column - 1
        first_row_column_value = first_row_column_id * (first_row_column_id + 1) // 2
        # Then subtract the row number to get our position
        position = first_row_column_value - self.row # Note: 0-based
        value = 20151125
        for n in range(position):
            value = (value * 252533) % 33554393
        return str(value)

    def solve2(self):
        pass

r = runner()

r.test('Sample', [
    'Enter the code at row 6, column 1.',
], '33071741')

r.run()
