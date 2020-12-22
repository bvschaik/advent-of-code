import adventofcode
from collections import deque

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(22)

    def reset(self):
        self.player1 = []
        self.player2 = []
        self.is_player1 = True

    def input_line(self, line):
        if not line:
            self.is_player1 = False
        elif not line.startswith("Player"):
            if self.is_player1:
                self.player1.append(int(line))
            else:
                self.player2.append(int(line))

    def solve1(self):
        p1 = deque(self.player1)
        p2 = deque(self.player2)

        while p1 and p2:
            v1 = p1.popleft()
            v2 = p2.popleft()
            if v1 > v2:
                p1.append(v1)
                p1.append(v2)
            else:
                p2.append(v2)
                p2.append(v1)
        return str(self.calculate_score(p1 + p2))

    def solve2(self):
        p1 = list(self.player1)
        p2 = list(self.player2)

        (id, winner) = self.play_recursive_game(p1, p2)
        return str(self.calculate_score(winner))

    def play_recursive_game(self, p1, p2):
        history = set()
        while p1 and p2:
            # 1: game ends when configuration has been seen before
            key = (tuple(p1), tuple(p2))
            if key in history:
                return (1, p1)
            history.add(key)
            # 2: each player draws a card
            v1 = p1.pop(0)
            v2 = p2.pop(0)
            if len(p1) >= v1 and len(p2) >= v2:
                # 3: recurse
                (winner, _) = self.play_recursive_game(list(p1[0:v1]), list(p2[0:v2]))
                if winner == 1:
                    p1.append(v1)
                    p1.append(v2)
                else:
                    p2.append(v2)
                    p2.append(v1)
            else:
                if v1 > v2:
                    p1.append(v1)
                    p1.append(v2)
                else:
                    p2.append(v2)
                    p2.append(v1)
        if p1:
            return (1, p1)
        else:
            return (2, p2)

    def calculate_score(self, values):
        mult = 1
        score = 0
        while values:
            v = values.pop()
            score += v * mult
            mult += 1
        return score

r = runner()

r.test('Sample 1', [
    'Player 1:',
    '9',
    '2',
    '6',
    '3',
    '1',
    '',
    'Player 2:',
    '5',
    '8',
    '4',
    '7',
    '10',
], '306')

r.run()
