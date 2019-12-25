import adventofcode
import intcode

NONE = -1
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

GO_LEFT = [LEFT, UP, RIGHT, DOWN]
GO_RIGHT = [RIGHT, DOWN, LEFT, UP]
DELTA = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(17)

    def reset(self):
        self.data = []

    def input_line(self, line):
        self.data = list(map(int, line.split(',')))

    def solve1(self):
        computer = intcode.ascii_computer(self.data)
        area = []
        for line in computer.lines():
            if not line:
                break
            area.append(line)

        total = 0
        for y in range(1, len(area) - 1):
            for x in range(1, len(area[y]) - 1):
                if area[y][x] == '#':
                    if (area[y][x-1] == '#' and area[y][x+1] == '#' and
                        area[y-1][x] == '#' and area[y+1][x] == '#'):
                        total += x * y
        return str(total)

    def solve2(self):
        self.data[0] = 2
        computer = intcode.ascii_computer(self.data)

        area = []
        for line in computer.lines():
            if not line:
                break
            area.append(line)

        (x, y, direction) = self.find_robot(area)

        x, y, direction, command = self.turn_and_move(x, y, direction, area)
        commands = [command]
        while direction != NONE:
            x, y, direction, command = self.turn_and_move(x, y, direction, area)
            if direction != NONE:
                commands.append(command)

        for cmd in self.split_program(commands):
            computer.write_line(cmd)
        computer.run()
        return str(computer.output[-1])

    def turn_and_move(self, x, y, direction, area):
        direction, turn = self.get_direction(x, y, direction, area)
        if direction != NONE:
            x, y, length = self.move(x, y, direction, area)
        else:
            length = 0
        return x, y, direction, (turn, length)

    def find_robot(self, area):
        for y, row in enumerate(area):
            for x, c in enumerate(row):
                if c == '^':
                    return (x, y, UP)
                if c == 'v':
                    return (x, y, DOWN)
                if c == '<':
                    return (x, y, LEFT)
                if c == '>':
                    return (x, y, RIGHT)
        assert False

    def get_direction(self, x, y, cur_dir, area):
        if cur_dir != RIGHT and x > 0 and area[y][x - 1] == '#':
            new_dir = LEFT
        elif cur_dir != LEFT and x < len(area[y]) - 1 and area[y][x + 1] == '#':
            new_dir = RIGHT
        elif cur_dir != DOWN and y > 0 and area[y - 1][x] == '#':
            new_dir = UP
        elif cur_dir != UP and y < len(area) - 1 and area[y + 1][x] == '#':
            new_dir = DOWN
        else:
            new_dir = NONE
        return new_dir, self.turn_direction(cur_dir, new_dir)

    def turn_direction(self, old_dir, new_dir):
        if GO_LEFT[old_dir] == new_dir:
            return 'L'
        elif GO_RIGHT[old_dir] == new_dir:
            return 'R'
        else:
            return '?'

    def move(self, x, y, direction, area):
        delta = DELTA[direction]
        length = 0
        x += delta[0]
        y += delta[1]
        max_x = len(area[0])
        max_y = len(area)
        while x >= 0 and x < max_x and y >= 0 and y < max_y and area[y][x] == '#':
            length += 1
            x += delta[0]
            y += delta[1]
        return (x - delta[0], y - delta[1], length)

    def split_program(self, commands):
        routine = []
        for i in range(6): # Max 5 commands on one line
            routine.append(commands[i])
            success, program = self.split_bc(self.replace_sublist(commands, routine, 'A'), routine)
            if success:
                return [
                    ','.join(map(lambda c: c[0], program[0])),
                    ','.join(map(lambda c: str.format('%s,%d' % c), program[1])),
                    ','.join(map(lambda c: str.format('%s,%d' % c), program[2])),
                    ','.join(map(lambda c: str.format('%s,%d' % c), program[3])),
                    'n'
                ]
        assert False

    def split_bc(self, commands, routine_a):
        offset = 0
        while commands[offset][0] == 'A':
            offset += 1
        routine_b = []
        for i in range(0, 6): # Max 5 commands
            if commands[i + offset][0] == 'A':
                break
            routine_b.append(commands[i + offset])
            success, main_program, routine_c = self.split_c(self.replace_sublist(commands, routine_b, 'B'))
            if success:
                return True, [main_program, routine_a, routine_b, routine_c]
        return False, []

    def split_c(self, commands):
        offset = 0
        while commands[offset][0] in 'AB':
            offset += 1
        routine = []
        for i in range(0, 6): # Max 5 commands
            if commands[i + offset][0] in 'AB':
                break
            routine.append(commands[i + offset])
            final = self.replace_sublist(commands, routine, 'C')
            if self.is_solution(final):
                return True, final, routine
        return False, None, None

    def is_solution(self, commands):
        for c in commands:
            if c[0] in 'RL':
                return False
        return True

    def replace_sublist(self, commands, routine, name):
        replaced = []
        i = 0
        while i < len(commands):
            if commands[i:i+len(routine)] == routine:
                replaced.append((name, 0))
                i += len(routine)
            else:
                replaced.append(commands[i])
                i += 1
        return replaced


r = runner()

r.run()
