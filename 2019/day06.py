import adventofcode
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(6)

    def reset(self):
        self.orbits = []

    def input_line(self, line):
        (inner, outer) = line.split(')')
        self.orbits.append((inner, outer))

    def solve1(self):
        system = defaultdict(list)
        for (inner, outer) in self.orbits:
            system[inner].append(outer)

        result = self.count_orbits(system, 'COM')
        return str(result)

    def count_orbits(self, system, obj, distance = 0):
        result = distance
        if obj in system:
            for outer in system[obj]:
                result += self.count_orbits(system, outer, distance + 1)
        return result

    def solve2(self):
        parents = dict()
        for (inner, outer) in self.orbits:
            parents[outer] = inner

        you_parents = self.path_to_com('YOU', parents)
        san_parents = self.path_to_com('SAN', parents)

        common_path = 0
        while you_parents[common_path] == san_parents[common_path]:
            common_path += 1

        return str(len(you_parents) + len(san_parents) - 2 * (common_path + 1))

    def path_to_com(self, start, parents):
        obj_parents = []
        obj = start
        while obj != 'COM':
            obj_parents.append(obj)
            obj = parents[obj]
        obj_parents.reverse()
        return obj_parents

r = runner()

r.test('Sample input', [
    'COM)B',
    'B)C',
    'C)D',
    'D)E',
    'E)F',
    'B)G',
    'G)H',
    'D)I',
    'E)J',
    'J)K',
    'K)L',
], '42')

r.test('Sample input 2', [
    'COM)B',
    'B)C',
    'C)D',
    'D)E',
    'E)F',
    'B)G',
    'G)H',
    'D)I',
    'E)J',
    'J)K',
    'K)L',
    'K)YOU',
    'I)SAN'
], None, '4')

r.run()
