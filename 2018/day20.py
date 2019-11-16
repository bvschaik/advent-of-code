from collections import defaultdict
from collections import deque
from runner import runner

class node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []
        self.distance = -1

class node_dict(defaultdict):
    def __init__(self):
        super().__init__(None) # base class doesn't get a factory

    def __missing__(self, key):
        val = node(key[0], key[1])
        self[key] = val
        return val

class day20(runner):
    def __init__(self):
        self.regex = ''

    def day(self):
        return 20

    def input(self, line):
        self.regex = line

    def solve1(self):
        # Remove starting ^ and replace end with ')' for easier programming
        route = self.regex[1:-1] + ')'

        all_nodes = node_dict()
        root = all_nodes[(0, 0)]
        self.create_maze(route, 0, [root], all_nodes)

        return str(self.dijkstra(root, all_nodes))

    def solve2(self):
        # Remove starting ^ and replace end with ')' for easier programming
        route = self.regex[1:-1] + ')'

        all_nodes = node_dict()
        root = all_nodes[(0, 0)]
        self.create_maze(route, 0, [root], all_nodes)
        self.dijkstra(root, all_nodes)

        return str(sum(map(lambda n: 1 if n.distance >= 1000 else 0, all_nodes.values())))

    def create_maze(self, route, index, start_nodes, all_nodes):
        nodes = list(start_nodes)
        while route[index] != ')' and route[index] != '|':
            c = route[index]
            index += 1
            if c == 'N':
                nodes = self.move_to(nodes, 0, -1, all_nodes)
            elif c == 'S':
                nodes = self.move_to(nodes, 0, 1, all_nodes)
            elif c == 'E':
                nodes = self.move_to(nodes, 1, 0, all_nodes)
            elif c == 'W':
                nodes = self.move_to(nodes, -1, 0, all_nodes)
            elif c == '(' or c == '|':
                (new_nodes, new_index) = self.create_maze(route, index, nodes, all_nodes)
                while route[new_index] != ')':
                    (more_nodes, new_index) = self.create_maze(route, new_index + 1, nodes, all_nodes)
                    new_nodes += more_nodes
                index = new_index + 1
        return (nodes, index)

    def move_to(self, nodes, dx, dy, all_nodes):
        result = []
        for n in nodes:
            to = all_nodes[(n.x + dx, n.y + dy)]
            # print("(%d, %d) => (%d, %d)" % (n.x, n.y, to.x, to.y))
            n.edges.append(to)
            to.edges.append(n)
            result.append(to)
        return result

    def dijkstra(self, root, all_nodes):
        root.distance = 0
        nodes_to_process = deque([root])
        max_distance = 0
        while nodes_to_process:
            node = nodes_to_process.popleft()
            if node.distance > max_distance:
                max_distance = node.distance
            for n in node.edges:
                if n.distance < 0:
                    n.distance = node.distance + 1
                    nodes_to_process.append(n)
        return max_distance

day20().test('Sample input', ['^WNE$'], '3')
day20().test('Recursion', ['^ENWWW(NEEE|SSE(EE|N))$'], '10')
day20().test('Extra sample 1', ['^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'], '23')
day20().test('Extra sample 2', ['^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'], '31')

day20().solve()
