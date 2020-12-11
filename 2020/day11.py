import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(11)

    def reset(self):
        self.seats = []

    def input_line(self, line):
        self.seats.append(line)

    def solve1(self):
        seatmap = self.create_seatmap()
        occupieds = [[0 for x in range(len(seatmap[0]))] for y in range(len(seatmap))]
        adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        height = len(seatmap) - 1
        width = len(seatmap[0]) - 1
        has_changes = True
        rounds = 0
        while has_changes:
            rounds += 1
            changes = []
            for y in range(1, height):
                for x in range(1, width):
                    if seatmap[y][x] != '.':
                        if seatmap[y][x] == 'L' and occupieds[y][x] == 0:
                            seatmap[y][x] = '#'
                            changes.append((x, y, 1))
                        elif seatmap[y][x] == '#' and occupieds[y][x] >= 4:
                            seatmap[y][x] = 'L'
                            changes.append((x, y, -1))
            for (x, y, change) in changes:
                for (dx, dy) in adjacents:
                    occupieds[y + dy][x + dx] += change
            has_changes = len(changes) > 0
        # print("equilibrium after %d rounds" % rounds)
        return str(sum(map(lambda r: sum(map(lambda s: s == '#', r)), seatmap)))

    def solve2(self):
        seatmap = self.create_seatmap()
        occupieds = [[0 for x in range(len(seatmap[0]))] for y in range(len(seatmap))]
        adjacents = [[[] for x in range(len(seatmap[0]))] for y in range(len(seatmap))]
        self.find_visible_adjacents(seatmap, adjacents)

        height = len(seatmap) - 1
        width = len(seatmap[0]) - 1
        has_changes = True
        rounds = 0
        while has_changes:
            rounds += 1
            changes = []
            for y in range(1, height):
                for x in range(1, width):
                    if seatmap[y][x] != '.':
                        if seatmap[y][x] == 'L' and occupieds[y][x] == 0:
                            seatmap[y][x] = '#'
                            changes.append((x, y, 1))
                        elif seatmap[y][x] == '#' and occupieds[y][x] >= 5:
                            seatmap[y][x] = 'L'
                            changes.append((x, y, -1))
            for (x, y, change) in changes:
                for (ax, ay) in adjacents[y][x]:
                    occupieds[ay][ax] += change
            has_changes = len(changes) > 0
        # print("equilibrium after %d rounds" % rounds)
        return str(sum(map(lambda r: sum(map(lambda s: s == '#', r)), seatmap)))

    def find_visible_adjacents(self, seatmap, adjacents):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for y in range(1, len(seatmap) - 1):
            for x in range(1, len(seatmap[y]) - 1):
                for (dx, dy) in directions:
                    nx = x + dx
                    ny = y + dy
                    while seatmap[ny][nx] == '.':
                        nx += dx
                        ny += dy
                    if seatmap[ny][nx] == 'L':
                        adjacents[y][x].append((nx, ny))

    def create_seatmap(self):
        empty = [' '] * (len(self.seats[0]) + 2)
        seatmap = [empty]
        for row in self.seats:
            seats = [' ']
            for c in row:
                seats.append(c)
            seats.append(' ')
            seatmap.append(seats)
        seatmap.append(list(empty))
        return seatmap

    def print(self, seatmap):
        for row in seatmap:
            for seat in row:
                print(seat, end = '')
            print()

r = runner()

r.test('Sample 1', [
    'L.LL.LL.LL',
    'LLLLLLL.LL',
    'L.L.L..L..',
    'LLLL.LL.LL',
    'L.LL.LL.LL',
    'L.LLLLL.LL',
    '..L.L.....',
    'LLLLLLLLLL',
    'L.LLLLLL.L',
    'L.LLLLL.LL',
], '37', '26')

r.run()
