import re
from runner import runner

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, x, y):
        return abs(x - self.x) + abs(y - self.y)

class area:
    def __init__(self):
        self.area = 0
        self.infinite = False

    def __repr__(self):
        return str.format("area(%d, %s)" % (self.area, self.infinite))

class day06(runner):
    def __init__(self, part2_threshold = 10000):
        self.points = []
        self.part2_threshold = part2_threshold

    def day(self):
        return 6
    
    def input(self, line):
        m = re.match(r'(\d+), (\d+)', line)
        self.points.append(point(int(m.group(1)), int(m.group(2))))

    def solve1(self):
        min_x = min(self.points, key = lambda p: p.x).x - 1
        max_x = max(self.points, key = lambda p: p.x).x + 1
        min_y = min(self.points, key = lambda p: p.y).y - 1
        max_y = max(self.points, key = lambda p: p.y).y + 1

        area_by_point = [area() for p in self.points]
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                min_point = -1
                min_dist = 10000000
                for (index, point) in enumerate(self.points):
                    dist = point.distance_to(x, y)
                    if dist < min_dist:
                        min_dist = dist
                        min_point = index
                    elif dist == min_dist:
                        min_point = -1
                if min_point >= 0:
                    area_by_point[min_point].area += 1
                    if x == min_x or x == max_x or y == min_y or y == max_y:
                        # Beyond border: if a point has minimum distance here, its area is infinite
                        area_by_point[min_point].infinite = True

        max_area = max(area_by_point, key = lambda a: a.area if not a.infinite else 0)
        return str(max_area.area)

    def solve2(self):
        min_x = min(self.points, key = lambda p: p.x).x - 1
        max_x = max(self.points, key = lambda p: p.x).x + 1
        min_y = min(self.points, key = lambda p: p.y).y - 1
        max_y = max(self.points, key = lambda p: p.y).y + 1

        num_points_in_region = 0
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                total_dist = 0
                for point in self.points:
                    total_dist += point.distance_to(x, y)
                if total_dist < self.part2_threshold:
                    num_points_in_region += 1
                
        return str(num_points_in_region)

day06(32).test('Sample input', [
    '1, 1',
    '1, 6',
    '8, 3',
    '3, 4',
    '5, 5',
    '8, 9',
], '17', '16')

day06().solve()
