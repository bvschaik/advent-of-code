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
                    break

                opponent = self.move_and_determine_opponent(u, units, cavern)

                # Attack
                if opponent and self.attack(opponent, cavern):
                    has_targets = self.determine_has_targets(units)

            units = list(filter(lambda u: u.hp > 0, units))

        completed_rounds = rounds - 1 if round_incomplete else rounds
        hp_remaining = sum(map(lambda u: u.hp, units))
        return str(completed_rounds * hp_remaining)

    def solve2(self):
        for elf_attack in range(4, 100):
            result = self.simulate_with_attack(elf_attack)
            if result:
                return result

    def simulate_with_attack(self, elf_attack):
        cavern = list(map(lambda x: list(x), self.start_map))
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
                    break

                opponent = self.move_and_determine_opponent(u, units, cavern)

                # Attack
                if opponent and self.attack(opponent, cavern, elf_attack if u.type == 'E' else 3):
                    has_targets = self.determine_has_targets(units)
                    if opponent.type == 'E':
                        return None

            units = list(filter(lambda u: u.hp > 0, units))

        completed_rounds = rounds - 1 if round_incomplete else rounds
        hp_remaining = sum(map(lambda u: u.hp, units))
        return str(completed_rounds * hp_remaining)

    def move_and_determine_opponent(self, u, units, cavern):
        opponent = self.opponent_in_range(u, units, cavern)
        if not opponent:
            next_tile = self.a_star(cavern, u.x, u.y, u.opponent)
            if next_tile:
                self.move_unit_to(u, next_tile[0], next_tile[1], cavern)
                opponent = self.opponent_in_range(u, units, cavern)
        return opponent

    def attack(self, opponent, cavern, attack = 3):
        opponent.hp -= attack
        if opponent.hp <= 0:
            cavern[opponent.y][opponent.x] = '.'
            return True
        return False

    def determine_has_targets(self, units):
        alive_types = set()
        for u in units:
            if u.hp > 0:
                alive_types.add(u.type)
        return len(alive_types) > 1

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

    def a_star(self, cavern, x, y, target):
        distances = [[-1 for xx in range(len(cavern[0]))] for yy in range(len(cavern))]
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
            return self.backtrack(target_tiles[0][1], target_tiles[0][0], distances)
        else:
            return None

    def evaluate_tile(self, cavern, distances, x, y, target, next_tiles):
        tile = cavern[y][x]
        if distances[y][x] < 0 and tile == '.':
            next_tiles.add((x, y))
        return tile == target

    def move_unit_to(self, u, next_x, next_y, cavern):
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

day15().test('Sample input', [
    '#######',
    '#.G...#',
    '#...EG#',
    '#.#.#G#',
    '#..G#E#',
    '#.....#',
    '#######',
], '27730', '4988')

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
], '39514', '31284')

day15().test('Example 3', [
    '#######', #       #######   
    '#E.G#.#', #       #G.G#.#   G(200), G(98)
    '#.#G..#', #       #.#G..#   G(200)
    '#G.#.G#', #  -->  #..#..#   
    '#G..#.#', #       #...#G#   G(95)
    '#...E.#', #       #...G.#   G(200)
    '#######', #       #######   
], '27755', '3478')

day15().test('Example 4', [
    '#######', #       #######   
    '#.E...#', #       #.....#   
    '#.#..G#', #       #.#G..#   G(200)
    '#.###.#', #  -->  #.###.#   
    '#E#G#G#', #       #.#.#.#   
    '#...#G#', #       #G.G#G#   G(98), G(38), G(200)
    '#######', #       #######   
], '28944', '6474')

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
], '18740', '1140')

day15().solve()
