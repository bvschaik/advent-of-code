import adventofcode
import re

INFINITE = 1000000000
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class node:
    def __init__(self, x, y, size, used, avail):
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.avail = avail

    def is_viable_pair(self, dst):
        return self.used > 0 and self.used <= dst.avail

class node_grid:
    def __init__(self, target, nodes):
        self.width = target.x + 1
        self.height = len(nodes) // self.width
        self.target_index = target.x
        empty_node = list(filter(lambda n: not n.used, nodes))[0]
        self.empty_index = empty_node.x + empty_node.y * self.width
        self.determine_passable(nodes)

    def determine_passable(self, nodes):
        used = [0] * len(nodes)
        avail = [0] * len(nodes)
        for n in nodes:
            index = n.x + n.y * self.width
            used[index] = n.used
            avail[index] = n.avail
            if not n.used:
                self.empty = index

        self.passable = [False] * len(nodes)
        for y in range(self.height):
            for x in range(self.width):
                index = y * self.width + x
                self.passable[index] = not self.is_wall_node(index, x, y, used, avail)

    def is_wall_node(self, index, x, y, used, avail):
        big_nodes = 0
        for d in DIRECTIONS:
            nx = d[0] + x
            ny = d[1] + y
            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
                n_index = nx + ny * self.width
                if used[index] > used[n_index] + avail[n_index]:
                    big_nodes += 1
        return big_nodes >= 2

    def path(self, from_index, to_index):
        distances = [0] * len(self.passable)
        distances[from_index] = 1
        changed = True
        while changed:
            changed = False
            for y in range(self.height):
                for x in range(self.width):
                    index = y * self.width + x
                    if distances[index] == 0 and self.update_path(index, x, y, distances):
                        changed = True
        return distances[to_index] - 1

    def update_path(self, index, x, y, distances):
        min_dist = INFINITE
        for d in DIRECTIONS:
            nx = d[0] + x
            ny = d[1] + y
            if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height and self.passable[index]:
                n_index = nx + ny * self.width
                if distances[n_index] and distances[n_index] + 1 < min_dist:
                    min_dist = distances[n_index] + 1
        if min_dist != INFINITE:
            distances[index] = min_dist
            return True
        return False

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(22)

    def reset(self):
        self.nodes = []

    def input_line(self, line):
        if not line.startswith('/dev'):
            return
        m = re.match(r'/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%', line)
        self.nodes.append(node(
            int(m.group(1)),
            int(m.group(2)),
            int(m.group(3)),
            int(m.group(4)),
            int(m.group(5))
        ))

    def solve1(self):
        total = 0
        for a in self.nodes:
            for b in self.nodes:
                if a != b and a.is_viable_pair(b):
                    total += 1
        return str(total)

    def solve2(self):
        # Nodes are interchangeable except for a 'wall' of high-capacity nodes in the middle
        # Minimum path:
        # a) get empty node to (target.x-1, 0) and move the target to that node
        # b) perform target.x-1 times a move forward, plus 4 * target.x-1 times
        # moving the empty node around the target

        grid = node_grid(self.get_target_node(), self.nodes)
        empty_to_target = grid.path(grid.empty_index, grid.target_index - 1) + 1;
        target_to_zero = grid.path(grid.target_index - 1, 0);

        return str(empty_to_target + 5 * target_to_zero);

    def get_target_node(self):
        return max(filter(lambda n: n.y == 0, self.nodes), key = lambda n: n.x)

r = runner()
r.run()
