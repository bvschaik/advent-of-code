import adventofcode

DOWN = (0, 1)
UP = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(19)

    def reset(self):
        self.diagram = []

    def input_line(self, line):
        self.diagram.append(line)

    def solve1(self):
        pos = (self.diagram[0].index('|'), 0)
        direction = DOWN
        letters = []
        steps = 0
        while True:
            pos = (pos[0] + direction[0], pos[1] + direction[1])
            steps += 1
            value = self.value(pos[0], pos[1])
            if value >= 'A' and value <= 'Z':
                letters.append(value)
            elif value == '+':
                if direction != LEFT and self.value(pos[0] + RIGHT[0], pos[1] + RIGHT[1]) != ' ':
                    direction = RIGHT
                elif direction != RIGHT and self.value(pos[0] + LEFT[0], pos[1] + LEFT[1]) != ' ':
                    direction = LEFT
                elif direction != DOWN and self.value(pos[0] + UP[0], pos[1] + UP[1]) != ' ':
                    direction = UP
                elif direction != UP and self.value(pos[0] + DOWN[0], pos[1] + DOWN[1]) != ' ':
                    direction = DOWN
                else:
                    break
            elif value == ' ':
                break
        self.steps = steps
        return ''.join(letters)

    def value(self, x, y):
        return self.diagram[y][x]

    def solve2(self):
        return str(self.steps)

r = runner()
r.run()
