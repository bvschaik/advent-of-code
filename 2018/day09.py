import re
from collections import deque
from runner import runner

class node:
    def __init__(self, id):
        self.id = id
        self.prev = None
        self.next = None

    def insert_after(self, n):
        self.next = n.next
        self.prev = n
        n.next.prev = self
        n.next = self
        return self

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.next

class day09(runner):
    def __init__(self):
        self.players = 0
        self.marbles = 0

    def day(self):
        return 9

    def input(self, line):
        m = re.match(r'(\d+) players; last marble is worth (\d+) points', line)
        self.players = int(m.group(1))
        self.marbles = int(m.group(2))

    def solve1(self):
        return str(self.simulate2(self.marbles))

    def solve2(self):
        return str(self.simulate2(self.marbles * 100))

    def simulate(self, max_marbles):
        scores = [0] * self.players
        nodes = [node(id) for id in range(0, max_marbles + 1)]

        current = nodes[0]
        current.prev = current
        current.next = current
        for m in range(1, max_marbles + 1):
            if m % 23 == 0:
                for _ in range(0, 7):
                    current = current.prev
                scores[m % self.players] += m + current.id
                current = current.remove()
            else:
                current = nodes[m].insert_after(current.next)
        return max(scores)

    def simulate2(self, max_marbles):
        scores = [0] * self.players

        q = deque()
        q.append(0)
        for m in range(1, max_marbles + 1):
            if m % 23 == 0:
                for _ in range(0, 7):
                    q.appendleft(q.pop())
                scores[m % self.players] += m + q.pop()
                q.append(q.popleft())
            else:
                q.append(q.popleft())
                q.append(m)
        return max(scores)

day09().test('Sample input', ['9 players; last marble is worth 25 points'], '32')
day09().test('Extra sample 1', ['10 players; last marble is worth 1618 points'], '8317')
day09().test('Extra sample 2', ['13 players; last marble is worth 7999 points'], '146373')
day09().test('Extra sample 3', ['17 players; last marble is worth 1104 points'], '2764')
day09().test('Extra sample 4', ['21 players; last marble is worth 6111 points'], '54718')
day09().test('Extra sample 5', ['30 players; last marble is worth 5807 points'], '37305')

day09().solve()
