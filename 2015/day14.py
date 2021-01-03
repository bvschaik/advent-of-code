import adventofcode
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(14)

    def configure(self, time = 2503):
        self.time = time

    def reset(self):
        self.reindeer = []

    def input_line(self, line):
        m = re.match(r'(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.', line)
        name = m.group(1)
        speed = int(m.group(2))
        fly_duration = int(m.group(3))
        rest_duration = int(m.group(4))
        total_duration = fly_duration + rest_duration
        self.reindeer.append((name, speed, fly_duration, total_duration))

    def solve1(self):
        time = self.time
        max_distance = 0
        for (name, speed, fly_duration, total_duration) in self.reindeer:
            distance = speed * fly_duration * (time // total_duration)
            remainder = time % total_duration
            if remainder > fly_duration:
                remainder = fly_duration
            distance += remainder * speed
            if distance > max_distance:
                max_distance = distance
        return str(max_distance)

    def solve2(self):
        points = [0] * len(self.reindeer)
        for t in range(1, self.time + 1):
            winners = self.get_winner(t)
            for w in winners:
                points[w] += 1

        return str(max(points))

    def get_winner(self, time):
        max_distance = 0
        max_reindeer = []
        for n, (name, speed, fly_duration, total_duration) in enumerate(self.reindeer):
            distance = speed * fly_duration * (time // total_duration)
            remainder = time % total_duration
            if remainder > fly_duration:
                remainder = fly_duration
            distance += remainder * speed
            if distance > max_distance:
                max_distance = distance
                max_reindeer = [n]
            elif distance >= max_distance:
                max_reindeer.append(n)
        return max_reindeer

r = runner()

r.configure(time = 1000)
r.test('Sample', [
    'Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.',
    'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.',
], '1120', '689')

r.configure()
r.run()
