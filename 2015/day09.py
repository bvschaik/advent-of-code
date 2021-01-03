import adventofcode
import re

INFINITY = 1000000

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(9)

    def reset(self):
        self.distances = dict()

    def input_line(self, line):
        m = re.match(r'(.*) to (.*) = (\d+)', line)
        city1 = m.group(1)
        city2 = m.group(2)
        distance = int(m.group(3))

        if not city1 in self.distances:
            self.distances[city1] = dict()
        if not city2 in self.distances:
            self.distances[city2] = dict()
        self.distances[city1][city2] = distance
        self.distances[city2][city1] = distance

    def solve1(self):
        all_cities = set(self.distances.keys())
        min_dist = INFINITY
        for city in self.distances:
            dist = self.visit_min(city, all_cities - {city})
            if dist < min_dist:
                min_dist = dist
        return str(min_dist)

    def visit_min(self, start_city, other_cities):
        if not other_cities:
            return 0
        min_dist = INFINITY
        for city in other_cities:
            dist = self.distances[start_city][city] + self.visit_min(city, other_cities - {city})
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def solve2(self):
        all_cities = set(self.distances.keys())
        max_dist = 0
        for city in self.distances:
            dist = self.visit_max(city, all_cities - {city})
            if dist > max_dist:
                max_dist = dist
        return str(max_dist)

    def visit_max(self, start_city, other_cities):
        if not other_cities:
            return 0
        max_dist = 0
        for city in other_cities:
            dist = self.distances[start_city][city] + self.visit_max(city, other_cities - {city})
            if dist > max_dist:
                max_dist = dist
        return max_dist

r = runner()

r.test('Sample', [
    'London to Dublin = 464',
    'London to Belfast = 518',
    'Dublin to Belfast = 141',
], '605', '982')

r.run()
