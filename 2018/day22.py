import adventofcode
import re
import heapq

infinity = 1000000000

neither = 0
torch = 1
climbing_gear = 2

class cave_map:
    def __init__(self, depth, target_x, target_y):
        self.depth = depth
        self.target_x = target_x
        self.target_y = target_y
        self.matrix = [[depth % 20183]]

    def type_at(self, x, y):
        while len(self.matrix) <= y:
            self.generate_row()
        while len(self.matrix[0]) <= x:
            self.generate_column()
        return self.matrix[y][x] % 3

    def generate_row(self):
        y = len(self.matrix)
        prev_row = self.matrix[-1]
        row = [(y * 48271 + self.depth) % 20183]
        for x in range(1, len(prev_row)):
            if x == self.target_x and y == self.target_y:
                erosion = self.depth % 20183
            else:
                erosion = (row[-1] * prev_row[x] + self.depth) % 20183
            row.append(erosion)
        self.matrix.append(row)

    def generate_column(self):
        x = len(self.matrix[0])
        self.matrix[0].append((x * 16807 + self.depth) % 20183)
        for y in range(1, len(self.matrix)):
            if x == self.target_x and y == self.target_y:
                erosion = self.depth % 20183
            else:
                erosion = (self.matrix[y][-1] * self.matrix[y-1][-1] + self.depth) % 20183
            self.matrix[y].append(erosion)

class node:
    def __init__(self, x, y, tool):
        self.x = x
        self.y = y
        self.tool = tool
        self.distance = infinity
        self.visited = False
        self.key = (x, y, tool)

    def create_neighbours(self, all_nodes, cave_map):
        neighbours = []
        # To the same node with a tool change
        node_type = cave_map.type_at(self.x, self.y)
        next_tool = (self.tool + 1) % 3
        if next_tool == node_type:
            next_tool = (next_tool + 1) % 3
        neighbours.append((self.add_node(all_nodes, self.x, self.y, next_tool), 7))

        # To adjacent nodes without tool change
        if self.can_move_to(cave_map, self.x - 1, self.y):
            neighbours.append((self.add_node(all_nodes, self.x - 1, self.y, self.tool), 1))
        if self.can_move_to(cave_map, self.x + 1, self.y):
            neighbours.append((self.add_node(all_nodes, self.x + 1, self.y, self.tool), 1))
        if self.can_move_to(cave_map, self.x, self.y - 1):
            neighbours.append((self.add_node(all_nodes, self.x, self.y - 1, self.tool), 1))
        if self.can_move_to(cave_map, self.x, self.y + 1):
            neighbours.append((self.add_node(all_nodes, self.x, self.y + 1, self.tool), 1))
        return neighbours

    def can_move_to(self, cave_map, x, y):
        if x < 0 or y < 0:
            return False
        # Going beyond 7 times the target will never be faster than changing tools every step of the way
        if x > 7 * cave_map.target_x:
            return False
        if y > 7 * cave_map.target_y:
            return False
        if cave_map.type_at(x, y) == self.tool:
            return False
        return True

    def add_node(self, all_nodes, x, y, tool):
        node_key = (x, y, tool)
        if node_key not in all_nodes:
            same_node = node(x, y, tool)
            all_nodes[node_key] = same_node
        return all_nodes[node_key]

    def __repr__(self):
        return str(self.key)

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(22)

    def reset(self):
        self.depth = 0
        self.target = (0, 0)

    def input_line(self, line):
        if line.startswith("depth: "):
            self.depth = int(line.split(' ')[1])
        else:
            m = re.match(r'target: (\d+),(\d+)', line)
            self.target = (int(m.group(1)), int(m.group(2)))

    def solve1(self):
        (target_x, target_y) = self.target
        risk = 0
        prev_erosion_row = []
        for y in range(target_y + 1):
            erosion_row = []
            for x in range(target_x + 1):
                if (x == 0 and y == 0) or (x == target_x and y == target_y):
                    erosion = self.depth % 20183
                elif y == 0:
                    erosion = (x * 16807 + self.depth) % 20183
                elif x == 0:
                    erosion = (y * 48271 + self.depth) % 20183
                else:
                    erosion = (erosion_row[-1] * prev_erosion_row[x] + self.depth) % 20183
                erosion_row.append(erosion)
                risk += erosion % 3
            prev_erosion_row = erosion_row
        return str(risk)

    def solve2(self):
        (target_x, target_y) = self.target
        cave = cave_map(self.depth, target_x, target_y)

        start = node(0, 0, torch)
        end = node(target_x, target_y, torch)

        all_nodes = dict()
        all_nodes[start.key] = start
        all_nodes[end.key] = end

        start.distance = 0
        heap = []
        heapq.heappush(heap, (start.distance, start.key, start))
        while heap:
            (_, _, u) = heapq.heappop(heap)
            if u.visited:
                continue

            if u == end:
                return str(u.distance)

            u.visited = True
            neighbours = u.create_neighbours(all_nodes, cave)
            for (n, dist) in neighbours:
                if not n.visited and u.distance + dist < n.distance:
                    n.distance = u.distance + dist
                    heapq.heappush(heap, (n.distance, n.key, n))

r = runner()
r.test('Sample input', ['depth: 510', 'target: 10,10'], '114', '45')

r.run()
