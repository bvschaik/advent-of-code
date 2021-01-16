import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(12)

    def reset(self):
        self.programs = []

    def input_line(self, line):
        (p, neighbours) = line.split(' <-> ')
        if int(p) == len(self.programs):
            self.programs.append(list(map(int, neighbours.split(', '))))
        else:
            print("uh?", line)

    def solve1(self):
        unvisited = set(range(1, len(self.programs)))
        visited = self.find_reachable(0, unvisited)
        return str(len(visited))

    def solve2(self):
        unvisited = set(range(0, len(self.programs)))
        groups = 0
        while unvisited:
            self.find_reachable(unvisited.pop(), unvisited)
            groups += 1
        return str(groups)

    def find_reachable(self, root, unvisited):
        visited = set()
        queue = {root}
        while queue:
            p = queue.pop()
            visited.add(p)
            for n in self.programs[p]:
                if n in unvisited:
                    unvisited.remove(n)
                    queue.add(n)
        return visited

r = runner()
r.run()
