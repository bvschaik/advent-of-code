import adventofcode
import heapq
from collections import defaultdict

def is_az(c):
    return c >= 'A' and c <= 'Z'

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(20)

    def reset(self):
        self.maze = []

    def input_line(self, line):
        self.maze.append(line)

    def solve1(self):
        distances = self.get_distance_graph(self.maze)
        return str(self.shortest_path(distances, 'AA', 'ZZ'))
        
    def shortest_path(self, distances, start_node, end_node):
        shortest_paths = dict()

        h = []
        heapq.heappush(h, (0, start_node))

        while h:
            (dist, to_node) = heapq.heappop(h)
            if to_node in shortest_paths:
                continue
            shortest_paths[to_node] = dist
            for n, dist in distances[to_node].items():
                heapq.heappush(h, (dist + 1 + shortest_paths[to_node], n))

        return shortest_paths[end_node] - 1 # Subtract portal cost from final node

    def get_distance_graph(self, maze):
        nodes = defaultdict(list)
        for y, row in enumerate(maze):
            for x, c in enumerate(row):
                if is_az(c):
                    if x + 1 < len(row) and is_az(row[x + 1]):
                        label = c + row[x + 1]
                        if x + 2 < len(row) and row[x + 2] == '.':
                            nodes[label].append((x + 2, y))
                        elif x > 0 and row[x - 1] == '.':
                            nodes[label].append((x - 1, y))
                    elif y + 1 < len(maze) and is_az(maze[y + 1][x]):
                        label = c + maze[y + 1][x]
                        if y + 2 < len(maze) and maze[y + 2][x] == '.':
                            nodes[label].append((x, y + 2))
                        elif y > 0 and maze[y - 1][x] == '.':
                            nodes[label].append((x, y - 1))

        node_positions = dict()
        for n, positions in nodes.items():
            for p in positions:
                node_positions[p] = n

        distances = defaultdict(dict)
        for p, label in node_positions.items():
            self.bfs(maze, node_positions, distances, label, p)
        return distances

    def bfs(self, maze, nodes, distances, label, start):
        visited = set()
        queue = [start]
        distance = 0
        while queue:
            new_queue = list()
            for p in queue:
                visited.add(p)
                if p in nodes:
                    to_label = nodes[p]
                    if label != to_label:
                        distances[label][to_label] = distance
                x, y = p
                if maze[y-1][x] == '.' and (x, y-1) not in visited:
                    new_queue.append((x, y-1))
                if maze[y+1][x] == '.' and (x, y+1) not in visited:
                    new_queue.append((x, y+1))
                if maze[y][x-1] == '.' and (x-1, y) not in visited:
                    new_queue.append((x-1, y))
                if maze[y][x+1] == '.' and (x+1, y) not in visited:
                    new_queue.append((x+1, y))
            queue = new_queue
            distance += 1

    def solve2(self):
        pass

r = runner()

r.test('Sample 1', [
    '         A           ',
    '         A           ',
    '  #######.#########  ',
    '  #######.........#  ',
    '  #######.#######.#  ',
    '  #######.#######.#  ',
    '  #######.#######.#  ',
    '  #####  B    ###.#  ',
    'BC...##  C    ###.#  ',
    '  ##.##       ###.#  ',
    '  ##...DE  F  ###.#  ',
    '  #####    G  ###.#  ',
    '  #########.#####.#  ',
    'DE..#######...###.#  ',
    '  #.#########.###.#  ',
    'FG..#########.....#  ',
    '  ###########.#####  ',
    '             Z       ',
    '             Z       ',
], '23')

r.test('Sample 2', [
    '                   A               ',
    '                   A               ',
    '  #################.#############  ',
    '  #.#...#...................#.#.#  ',
    '  #.#.#.###.###.###.#########.#.#  ',
    '  #.#.#.......#...#.....#.#.#...#  ',
    '  #.#########.###.#####.#.#.###.#  ',
    '  #.............#.#.....#.......#  ',
    '  ###.###########.###.#####.#.#.#  ',
    '  #.....#        A   C    #.#.#.#  ',
    '  #######        S   P    #####.#  ',
    '  #.#...#                 #......VT',
    '  #.#.#.#                 #.#####  ',
    '  #...#.#               YN....#.#  ',
    '  #.###.#                 #####.#  ',
    'DI....#.#                 #.....#  ',
    '  #####.#                 #.###.#  ',
    'ZZ......#               QG....#..AS',
    '  ###.###                 #######  ',
    'JO..#.#.#                 #.....#  ',
    '  #.#.#.#                 ###.#.#  ',
    '  #...#..DI             BU....#..LF',
    '  #####.#                 #.#####  ',
    'YN......#               VT..#....QG',
    '  #.###.#                 #.###.#  ',
    '  #.#...#                 #.....#  ',
    '  ###.###    J L     J    #.#.###  ',
    '  #.....#    O F     P    #.#...#  ',
    '  #.###.#####.#.#####.#####.###.#  ',
    '  #...#.#.#...#.....#.....#.#...#  ',
    '  #.#####.###.###.#.#.#########.#  ',
    '  #...#.#.....#...#.#.#.#.....#.#  ',
    '  #.###.#####.###.###.#.#.#######  ',
    '  #.#.........#...#.............#  ',
    '  #########.###.###.#############  ',
    '           B   J   C               ',
    '           U   P   P               ',
], '58')

r.run()
