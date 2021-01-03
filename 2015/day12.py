import adventofcode
import json
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(12)

    def reset(self):
        self.json = None

    def input_line(self, line):
        self.json = line

    def solve1(self):
        m = re.findall(r'(-?\d+)', self.json)
        return str(sum(map(int, m)))

    def solve2(self):
        data = json.loads(self.json)
        return str(self.sum_numbers(data))
        
    def sum_numbers(self, node):
        if type(node) is list:
            return sum(map(lambda n: self.sum_numbers(n), node))
        elif type(node) is dict:
            if "red" in node.values():
                return 0
            else:
                return sum(map(lambda n: self.sum_numbers(n), node.values()))
        elif type(node) is int:
            return node
        else:
            return 0

r = runner()

r.test('Sample 1', ['[1,2,3]'], '6')
r.test('Sample 2', ['{"a":2,"b":4}'], '6')
r.test('Sample 3', ['[[[3]]]'], '3')
r.test('Sample 4', ['{"a":{"b":4},"c":-1}'], '3')

r.run()
