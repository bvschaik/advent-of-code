import adventofcode
import string

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(18)

    def reset(self):
        self.maze = []
        self.cache_hits = 0

    def input_line(self, line):
        self.maze.append(line)

    def solve1(self):
        all_distances = self.get_all_distances(self.find('@'))

        cache = dict()
        minimum_distance = self.solve_with_cache(all_distances, '@', frozenset(all_distances.keys()) - {'@'}, cache)
        # print('Cache hits:', self.cache_hits)
        # print('Cache size:', len(cache))
        return str(minimum_distance)

    def solve_with_cache(self, all_distances, from_node, keys_to_go = frozenset(), cache = dict()):
        if not keys_to_go:
            return 0

        cache_key = (from_node, keys_to_go)
        if cache_key in cache:
            self.cache_hits += 1
            return cache[cache_key]

        distances = all_distances[from_node]
        min_dist = 100000000
        for key in keys_to_go:
            if not distances[key][1].intersection(keys_to_go):
                dist = distances[key][0] + self.solve_with_cache(all_distances, key, keys_to_go - {key}, cache)
                if dist < min_dist:
                    min_dist = dist

        cache[cache_key] = min_dist
        return min_dist

    def solve2(self):
        at_x, at_y = self.find('@')

        self.maze[at_y] = self.maze[at_y][:at_x-1] + '###' + self.maze[at_y][at_x + 2:]
        self.maze[at_y-1] = self.maze[at_y-1][:at_x-1] + '@#@' + self.maze[at_y-1][at_x + 2:]
        self.maze[at_y+1] = self.maze[at_y+1][:at_x-1] + '@#@' + self.maze[at_y+1][at_x + 2:]

        robot1 = self.get_all_distances((at_x - 1, at_y - 1))
        robot2 = self.get_all_distances((at_x + 1, at_y - 1))
        robot3 = self.get_all_distances((at_x - 1, at_y + 1))
        robot4 = self.get_all_distances((at_x + 1, at_y + 1))
        all_distances = [robot1, robot2, robot3, robot4]
        robot_keys = dict()
        for i, r in enumerate(all_distances):
            for c in r.keys():
                if c != '@':
                    robot_keys[c] = i

        from_nodes = ['@', '@', '@', '@']
        min_distance = self.solve2_with_cache(all_distances, robot_keys, from_nodes, frozenset(robot_keys.keys()))
        return str(min_distance)

    def solve2_with_cache(self, all_distances, robot_keys, from_nodes, keys_to_go = frozenset(), cache = dict()):
        if not keys_to_go:
            return 0

        cache_key = (tuple(from_nodes), keys_to_go)
        if cache_key in cache:
            return cache[cache_key]

        min_dist = 100000000
        for key in keys_to_go:
            robot = robot_keys[key]
            (distance, doors) = all_distances[robot][from_nodes[robot]][key]
            if not doors.intersection(keys_to_go):
                old_from = from_nodes[robot]
                from_nodes[robot] = key
                dist = distance + self.solve2_with_cache(all_distances, robot_keys, from_nodes, keys_to_go - {key}, cache)
                from_nodes[robot] = old_from
                if dist < min_dist:
                    min_dist = dist

        cache[cache_key] = min_dist
        return min_dist

    def get_all_distances(self, start):
        reachable = self.get_distances(start)
        all_distances = dict()
        all_distances['@'] = reachable
        for c in reachable.keys():
            dist = self.get_distances(self.find(c))
            if dist:
                all_distances[c] = dist
        return all_distances

    def get_distances(self, start):
        distances = dict()
        maze = [list(p) for p in self.maze]
        queue = dict()
        queue[start] = set()
        distance = 0
        while queue:
            new_queue = dict()
            for x, y in queue:
                doors = queue[(x, y)]
                if maze[y][x] >= 'a' and maze[y][x] <= 'z':
                    distances[maze[y][x]] = (distance, doors)
                maze[y][x] = '!'
                self.evaluate(maze, x, y + 1, doors, new_queue)
                self.evaluate(maze, x, y - 1, doors, new_queue)
                self.evaluate(maze, x + 1, y, doors, new_queue)
                self.evaluate(maze, x - 1, y, doors, new_queue)
            queue = new_queue
            distance += 1
        return distances

    def evaluate(self, maze, x, y, doors, queue):
        val = maze[y][x]
        if val >= 'a' and val <= 'z':
            queue[(x, y)] = doors
        elif val >= 'A' and val <= 'Z':
            new_doors = set(doors)
            new_doors.add(str.lower(val))
            queue[(x, y)] = new_doors
        elif val == '.' or val == '@':
            queue[(x, y)] = doors

    def find(self, c):
        for y in range(len(self.maze)):
            row = self.maze[y]
            for x in range(len(row)):
                if row[x] == c:
                    return (x, y)
        return (-1, -1)

r = runner()

# r.test('Sample 2', [
#     '########################',
#     '#...............b.C.D.f#',
#     '#.######################',
#     '#.....@.a.B.c.d.A.e.F.g#',
#     '########################',
# ], '132')

# r.test('Sample 3', [
#     '#################',
#     '#i.G..c...e..H.p#',
#     '########.########',
#     '#j.A..b...f..D.o#',
#     '########@########',
#     '#k.E..a...g..B.n#',
#     '########.########',
#     '#l.F..d...h..C.m#',
#     '#################',
# ], '136')

# r.test('Sample 4', [
#     '########################',
#     '#@..............ac.GI.b#',
#     '###d#e#f################',
#     '###A#B#C################',
#     '###g#h#i################',
#     '########################',
# ], '81')

r.test('Sample 2.1', [
    '#######',
    '#a.#Cd#',
    '##...##',
    '##.@.##',
    '##...##',
    '#cB#Ab#',
    '#######',
], None, '8')

r.test('Sample 2.2', [
    '###############',
    '#d.ABC.#.....a#',
    '######...######',
    '######.@.######',
    '######...######',
    '#b.....#.....c#',
    '###############',
], None, '24')

r.test('Sample 2.3', [
    '#############',
    '#DcBa.#.GhKl#',
    '#.###...#I###',
    '#e#d#.@.#j#k#',
    '###C#...###J#',
    '#fEbA.#.FgHi#',
    '#############',
], None, '32')

r.test('Sample 2.4', [
    '#############',
    '#g#f.D#..h#l#',
    '#F###e#E###.#',
    '#dCba...BcIJ#',
    '#####.@.#####',
    '#nK.L...G...#',
    '#M###N#H###.#',
    '#o#m..#i#jk.#',
    '#############',
], None, '72')

r.run()
