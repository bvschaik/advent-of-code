import adventofcode

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(1)

    def reset(self):
        self.instructions = []

    def input_line(self, line):
        for instr in line.split(', '):
            self.instructions.append((instr[0], int(instr[1:])))

    def solve1(self):
        position = (0, 0)
        direction = 0
        for n in self.instructions:
            if n[0] == 'R':
                direction = (direction + 1) % 4
            elif n[0] == 'L':
                direction = (direction - 1) % 4
            position = (
                position[0] + n[1] * DIRECTIONS[direction][0],
                position[1] + n[1] * DIRECTIONS[direction][1]
            )
        return position[0] + position[1]

    def solve2(self):
        position = (0, 0)
        visited = {position}
        direction = 0
        for instr in self.instructions:
            if instr[0] == 'R':
                direction = (direction + 1) % 4
            elif instr[0] == 'L':
                direction = (direction - 1) % 4
            
            for i in range(instr[1]):
                position = (
                    position[0] + DIRECTIONS[direction][0],
                    position[1] + DIRECTIONS[direction][1]
                )
                if position in visited:
                    return str(position[0] + position[1])
                visited.add(position)

r = runner()

r.test('Sample 2', ['R8, R4, R4, R8'], None, '4')

r.run()
