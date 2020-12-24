import adventofcode
from collections import defaultdict

EAST = (1, 0, -1)
WEST = (-1, 0, 1)
NORTHEAST = (1, -1, 0)
SOUTHWEST = (-1, 1, 0)
NORTHWEST = (0, -1, 1)
SOUTHEAST = (0, 1, -1)

ALL_DIRECTIONS = [EAST, WEST, NORTHEAST, NORTHWEST, SOUTHEAST, SOUTHWEST]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(24)

    def reset(self):
        self.input = []

    def input_line(self, line):
        self.input.append(line)

    def solve1(self):
        self.tiles = set()
        for line in self.input:
            tile = self.follow_line(line)
            if tile in self.tiles:
                self.tiles.remove(tile)
            else:
                self.tiles.add(tile)
        return str(len(self.tiles))

    def follow_line(self, line):
        prev = None
        tile = (0, 0, 0)
        for c in line:
            if c == 'e':
                if prev == 'n':
                    delta = NORTHEAST
                elif prev == 's':
                    delta = SOUTHEAST
                else:
                    delta = EAST
            elif c == 'w':
                if prev == 'n':
                    delta = NORTHWEST
                elif prev == 's':
                    delta = SOUTHWEST
                else:
                    delta = WEST
            else:
                prev = c
                continue
            tile = (tile[0] + delta[0], tile[1] + delta[1], tile[2] + delta[2])
            prev = None
        return tile

    def solve2(self):
        neighbours = defaultdict(int)
        for t in self.tiles:
            for d in ALL_DIRECTIONS:
                n = (t[0] + d[0], t[1] + d[1], t[2] + d[2])
                neighbours[n] += 1
        black = self.tiles
        for day in range(100):
            changes = []
            for t in black:
                n = neighbours[t]
                if n == 0 or n > 2:
                    changes.append((t, -1))
            for t in neighbours:
                if neighbours[t] == 2 and t not in black:
                    changes.append((t, 1))
            for t, delta in changes:
                if delta == -1:
                    black.remove(t)
                else:
                    black.add(t)
                for d in ALL_DIRECTIONS:
                    n = (t[0] + d[0], t[1] + d[1], t[2] + d[2])
                    neighbours[n] += delta
        return str(len(black))

r = runner()

r.test('Sample 1', [
    'sesenwnenenewseeswwswswwnenewsewsw',
    'neeenesenwnwwswnenewnwwsewnenwseswesw',
    'seswneswswsenwwnwse',
    'nwnwneseeswswnenewneswwnewseswneseene',
    'swweswneswnenwsewnwneneseenw',
    'eesenwseswswnenwswnwnwsewwnwsene',
    'sewnenenenesenwsewnenwwwse',
    'wenwwweseeeweswwwnwwe',
    'wsweesenenewnwwnwsenewsenwwsesesenwne',
    'neeswseenwwswnwswswnw',
    'nenwswwsewswnenenewsenwsenwnesesenew',
    'enewnwewneswsewnwswenweswnenwsenwsw',
    'sweneswneswneneenwnewenewwneswswnese',
    'swwesenesewenwneswnwwneseswwne',
    'enesenwswwswneneswsenwnewswseenwsese',
    'wnwnesenesenenwwnenwsewesewsesesew',
    'nenewswnwewswnenesenwnesewesw',
    'eneswnwswnwsenenwnwnwwseeswneewsenese',
    'neswnwewnwnwseenwseesewsenwsweewe',
    'wseweeenwnesenwwwswnew',
], '10')

r.run()
