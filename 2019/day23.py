import adventofcode
import intcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(23)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computers = [intcode.computer(self.data, [i]) for i in range(50)]
        queue = [[] for _ in range(50)]
        
        while True:
            for i, c in enumerate(computers):
                #print("Running", i)
                if queue[i]:
                    x, y = queue[i].pop(0)
                    c.input.append(x)
                    c.input.append(y)
                result = c.run_until_io()
                if result == 'input':
                    c.input.append(-1)
                elif result == 'output':
                    dst = c.output[-1]
                    x = c.run_until_output()
                    y = c.run_until_output()
                    if dst == 255:
                        return str(y)
                    queue[dst].append((x, y))

    def solve2(self):
        pass

r = runner()

r.run()
