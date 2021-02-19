import adventofcode
from collections import deque

INFINITY = 100000000

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(24)

    def reset(self):
        self.grid = []

    def input_line(self, line):
        self.grid.append(line)

    def solve1(self):
        self.build_matrix()
        return str(self.run_tsp(False))

    def solve2(self):
        return str(self.run_tsp(True))

    def build_matrix(self):
        points = dict()
        for y, row in enumerate(self.grid):
            for x, c in enumerate(row):
                if c != '.' and c != '#':
                    points[int(c)] = (x, y)
        self.distances = [[0] * len(points) for x in range(len(points))]
        for i, p in points.items():
            distances_from_p = self.find_distances_from(p)
            for j, q in points.items():
                self.distances[i][j] = distances_from_p[q]

    def find_distances_from(self, p):
        distances = dict()
        queue = deque()
        queue.append((p, 0))
        while queue:
            (p, dist) = queue.popleft()
            if self.grid[p[1]][p[0]] != '#' and p not in distances:
                distances[p] = dist
                queue.append(((p[0] - 1, p[1]), dist + 1))
                queue.append(((p[0] + 1, p[1]), dist + 1))
                queue.append(((p[0], p[1] - 1), dist + 1))
                queue.append(((p[0], p[1] + 1), dist + 1))
        return distances

    def run_tsp(self, return_to_zero):
        self.min_distance = INFINITY
        visited = {0}
        self.travel(0, return_to_zero, visited)
        return self.min_distance

    def travel(self, from_id, return_to_zero, visited, distance = 0):
        if len(visited) == len(self.distances):
            if return_to_zero:
                distance += self.distances[from_id][0]
            if distance < self.min_distance:
                self.min_distance = distance
            return
        if distance >= self.min_distance:
            return
        for to_id in range(len(self.distances)):
            if to_id not in visited:
                visited.add(to_id)
                self.travel(to_id, return_to_zero, visited, distance + self.distances[from_id][to_id])
                visited.remove(to_id)

r = runner()
r.run()
