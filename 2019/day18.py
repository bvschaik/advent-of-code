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
        all_distances = dict()
        all_distances['@'] = self.get_distances('@')
        for c in string.ascii_lowercase:
            dist = self.get_distances(c)
            if dist:
                all_distances[c] = dist

        # for from_node, distances in all_distances.items():
        #     for to_node, (dist, doors) in distances.items():
        #         print("%s to %s: %d doors %s" % (from_node, to_node, dist, ''.join(doors)))

        cache = dict()
        minimum_distance = self.solve_with_cache(all_distances, '@', set(all_distances.keys()) - {'@'}, cache)
        # print('Cache hits:', self.cache_hits)
        # print('Cache size:', len(cache))
        return str(minimum_distance)

    def solve_with_cache(self, all_distances, from_node, keys_to_go = set(), cache = dict()):
        if not keys_to_go:
            return 0

        cache_key = (from_node, tuple(keys_to_go))
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

    def get_distances(self, from_node):
        distances = dict()

        maze = [list(p) for p in self.maze]
        start = self.find(maze, from_node)
        if start[0] < 0:
            return None

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

    def find(self, maze, c):
        for y in range(len(maze)):
            row = maze[y]
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

r.run()
