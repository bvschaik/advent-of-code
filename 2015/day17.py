import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(17)

    def configure(self, target = 150):
        self.target = target

    def reset(self):
        self.containers = []

    def input_line(self, line):
        self.containers.append(int(line))

    def solve1(self):
        containers = list(sorted(self.containers))
        combinations = self.combinations(containers, self.target)
        return str(combinations)

    def combinations(self, containers, target):
        if target == 0:
            return 1
        if not containers:
            return 0
        options = 0
        container = containers[-1]
        if container <= target:
            options += self.combinations(containers[0:-1], target - container)
        options += self.combinations(containers[0:-1], target)
        return options

    def solve2(self):
        self.min_used = len(self.containers)
        self.min_combinations = 0
        containers = list(sorted(self.containers))
        self.min_container_combinations(containers, self.target, [])
        return str(self.min_combinations)

    def min_container_combinations(self, containers, target, used):
        if target == 0:
            if len(used) < self.min_used:
                self.min_used = len(used)
                self.min_combinations = 1
            elif len(used) == self.min_used:
                self.min_combinations += 1
            return
        if not containers:
            return
        if len(used) > self.min_used:
            return
        container = containers[-1]
        if container <= target:
            used.append(container)
            self.min_container_combinations(containers[0:-1], target - container, used)
            used.pop()
        self.min_container_combinations(containers[0:-1], target, used)

r = runner()

r.configure(25)
r.test('Sample', [
    '20',
    '15',
    '10',
    '5',
    '5',
], '4', '3')

r.configure()
r.run()
