import adventofcode
import assembunny

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(25)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        self.instructions.append(line)

    def solve1(self):
        comp = assembunny.computer(self.instructions).optimize_mul()
        for i in range(1000):
            # print(i)
            output = []
            comp.reset()
            comp.registers['a'] = i
            last_x = 1
            count = 0
            for x in comp.run_with_output():
                if x != 1 - last_x:
                    break
                last_x = x
                count += 1
                if count >= 10:
                    return str(i)

    def solve2(self):
        pass

r = runner()
r.run()
