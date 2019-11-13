from runner import runner

class unit_data:
    def __init__(self, type, x, y):
        self.type = type
        self.opponent = 'G' if type == 'E' else 'E'
        self.x = x
        self.y = y
        self.hp = 200

    def __repr__(self):
        return str.format("unit(%s, x=%d, y=%d, hp=%d)" % (self.type, self.x, self.y, self.hp))

class day15(runner):
    def __init__(self):
        self.start_map = []

    def day(self):
        return 15

    def input(self, line):
        self.start_map.append(line)

    def solve1(self):
        cavern = list(map(lambda x: list(x), self.start_map))
        distances = [[0 for x in range(len(cavern[0]))] for y in range(len(cavern))]
        units = self.init_units(cavern)

        rounds = 0
        has_targets = True
        round_incomplete = False
        while has_targets:
            rounds += 1
            units.sort(key = lambda u: (u.y, u.x))
            for u in units:
                if u.hp <= 0:
                    continue
                if not has_targets:
                    round_incomplete = True
                    continue
                opponent = self.opponent_in_range(u, units, cavern)
                if not opponent:
                    target_tile = self.a_star(cavern, distances, u.x, u.y, u.opponent)
                    if target_tile:
                        self.move_unit_toward(u, target_tile[0], target_tile[1], cavern, distances)
                        opponent = self.opponent_in_range(u, units, cavern)

                # Attack
                if opponent:
                    opponent.hp -= 3
                    if opponent.hp <= 0:
                        cavern[opponent.y][opponent.x] = '.'
                        alive_types = set()
                        for u in units:
                            if u.hp > 0:
                                alive_types.add(u.type)
                        has_targets = len(alive_types) > 1
            units = list(filter(lambda u: u.hp > 0, units))

            #print(rounds)
            #self.print_map(cavern, units)
        completed_rounds = rounds - 1 if round_incomplete else rounds
        hp_remaining = sum(map(lambda u: u.hp, units))
        # print(units)
        # print("Completed rounds: %d, HP remaining %d" % (completed_rounds, hp_remaining))
        return str(completed_rounds * hp_remaining)

    def print_map(self, cavern, units):
        for (y, row) in enumerate(cavern):
            for x in row:
                print(x, end = '')
            print("    ", end = '')
            for u in units:
                if u.y == y:
                    print(" %d" % (u.hp), end = '')
            print()

    def init_units(self, cavern):
        units = []
        for y in range(len(cavern)):
            line = cavern[y]
            for x in range(len(line)):
                c = line[x]
                if c == 'G' or c == 'E':
                    units.append(unit_data(c, x, y))
        return units

    def opponent_in_range(self, u, units, cavern):
        opponents = []
        if cavern[u.y - 1][u.x] == u.opponent:
            opponents.append(self.find_unit(units, u.x, u.y - 1))
        if cavern[u.y][u.x - 1] == u.opponent:
            opponents.append(self.find_unit(units, u.x - 1, u.y))
        if cavern[u.y][u.x + 1] == u.opponent:
            opponents.append(self.find_unit(units, u.x + 1, u.y))
        if cavern[u.y + 1][u.x] == u.opponent:
            opponents.append(self.find_unit(units, u.x, u.y + 1))
        min_opponent = None
        for o in opponents:
            if not min_opponent or min_opponent.hp > o.hp:
                min_opponent = o
        return min_opponent

    def find_unit(self, units, x, y):
        for u in units:
            if u.x == x and u.y == y and u.hp > 0:
                return u
        return None

    def a_star(self, cavern, distances, x, y, target):
        for row in distances:
            for n in range(len(row)):
                row[n] = -1
        d = 0
        tiles = set([(x, y)])
        target_tiles = []
        while not target_tiles and tiles:
            next_tiles = set()
            for (x, y) in tiles:
                distances[y][x] = d
                if self.evaluate_tile(cavern, distances, x, y - 1, target, next_tiles):
                    target_tiles.append((y, x))
                if self.evaluate_tile(cavern, distances, x - 1, y, target, next_tiles):
                    target_tiles.append((y, x))
                if self.evaluate_tile(cavern, distances, x + 1, y, target, next_tiles):
                    target_tiles.append((y, x))
                if self.evaluate_tile(cavern, distances, x, y + 1, target, next_tiles):
                    target_tiles.append((y, x))
            tiles = next_tiles
            d += 1
        if target_tiles:
            target_tiles.sort()
            return (target_tiles[0][1], target_tiles[0][0])
        else:
            return None

    def evaluate_tile(self, cavern, distances, x, y, target, next_tiles):
        tile = cavern[y][x]
        if distances[y][x] < 0 and tile == '.':
            next_tiles.add((x, y))
        return tile == target

    def move_unit_toward(self, u, x, y, cavern, distances):
        (next_x, next_y) = self.backtrack(x, y, distances)
        cavern[u.y][u.x] = '.'
        cavern[next_y][next_x] = u.type
        u.x = next_x
        u.y = next_y

    def backtrack(self, x, y, distances):
        d = distances[y][x]
        tiles = set([(x, y)])
        while d > 1:
            next_tiles = set()
            d -= 1
            for (x, y) in tiles:
                if distances[y - 1][x] == d:
                    next_tiles.add((x, y - 1))
                if distances[y][x - 1] == d:
                    next_tiles.add((x - 1, y))
                if distances[y][x + 1] == d:
                    next_tiles.add((x + 1, y))
                if distances[y + 1][x] == d:
                    next_tiles.add((x, y + 1))
            tiles = next_tiles
        sorted_tiles = sorted(tiles, key = lambda p: (p[1], p[0]))
        return sorted_tiles[0]

    def solve2(self):
        pass

day15().test('Sample input', [
    '#######',
    '#.G...#',
    '#...EG#',
    '#.#.#G#',
    '#..G#E#',
    '#.....#',
    '#######',
], '27730')

day15().test('Example 1', [
    '#######', #       #######
    '#G..#E#', #       #...#E#   E(200)
    '#E#E.E#', #       #E#...#   E(197)
    '#G.##.#', #  -->  #.E##.#   E(185)
    '#...#E#', #       #E..#E#   E(200), E(200)
    '#...E.#', #       #.....#
    '#######', #       #######
], '36334')

day15().test('Example 2', [
    '#######', #       #######   
    '#E..EG#', #       #.E.E.#   E(164), E(197)
    '#.#G.E#', #       #.#E..#   E(200)
    '#E.##E#', #  -->  #E.##.#   E(98)
    '#G..#.#', #       #.E.#.#   E(200)
    '#..E#.#', #       #...#.#
    '#######', #       #######
], '39514')

day15().test('Example 3', [
    '#######', #       #######   
    '#E.G#.#', #       #G.G#.#   G(200), G(98)
    '#.#G..#', #       #.#G..#   G(200)
    '#G.#.G#', #  -->  #..#..#   
    '#G..#.#', #       #...#G#   G(95)
    '#...E.#', #       #...G.#   G(200)
    '#######', #       #######   
], '27755')

day15().test('Example 4', [
    '#######', #       #######   
    '#.E...#', #       #.....#   
    '#.#..G#', #       #.#G..#   G(200)
    '#.###.#', #  -->  #.###.#   
    '#E#G#G#', #       #.#.#.#   
    '#...#G#', #       #G.G#G#   G(98), G(38), G(200)
    '#######', #       #######   
], '28944')

day15().test('Example 5', [
    '#########', #
    '#G......#', #G(137)
    '#.E.#...#', #G(200), G(200)
    '#..##..G#', #G(200)
    '#...##..#', #
    '#...#...#', #G(200)
    '#.G...G.#', #
    '#.....G.#', #
    '#########', #
], '18740')

day15().solve()
