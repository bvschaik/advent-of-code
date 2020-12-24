import adventofcode

class node_ring:
    def __init__(self, first_numbers, max_value):
        self.max_value = max_value
        self.nodes = [0] * (max_value + 1)

        prev = max_value
        if max_value <= len(first_numbers):
            prev = first_numbers[-1]
        for n in first_numbers:
            self.nodes[prev] = n
            prev = n
        for n in range(len(first_numbers) + 1, max_value + 1):
            self.nodes[prev] = n
            prev = n
        self.current = first_numbers[0]

    def move(self, times = 1):
        for x in range(times):
            n1 = self.nodes[self.current]
            n2 = self.nodes[n1]
            n3 = self.nodes[n2]
            next_value = self.current
            while True:
                next_value -= 1
                if next_value == 0:
                    next_value = self.max_value
                if next_value != n1 and next_value != n2 and next_value != n3:
                    break
            self.nodes[self.current] = self.nodes[n3]
            self.nodes[n3] = self.nodes[next_value]
            self.nodes[next_value] = n1
            self.current = self.nodes[self.current]

    def print(self):
        start_value = self.current
        print(start_value, end = '')
        n = start_value
        while self.nodes[n] != start_value:
            n = self.nodes[n]
            print('-', end = '')
            print(n, end = '')
        print()

    def solution1(self):
        n = self.nodes[1]
        result = []
        while n != 1:
            result.append(str(n))
            n = self.nodes[n]
        return ''.join(result)

    def solution2(self):
        print(self.nodes[1], self.nodes[self.nodes[1]])
        return self.nodes[1] * self.nodes[self.nodes[1]]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(23)

    def reset(self):
        self.input = []

    def input_line(self, line):
        self.input = list(map(int, line))

    def solve1(self):
        ring = node_ring(self.input, 9)
        ring.move(100)
        return str(ring.solution1())

    def solve2(self):
        ring = node_ring(self.input, 1000000)
        ring.move(10000000)
        return str(ring.solution2())

r = runner()

r.test('Sample 1', ['389125467'], '67384529')

r.run()
