import adventofcode

MAX_IP = 4294967296

class ip_range:
    def __init__(self, from_ip, to_ip):
        # to_ip is exclusive
        self.from_ip = from_ip
        self.to_ip = to_ip

    def intersects(self, other):
        return other.from_ip <= self.to_ip and other.to_ip >= self.from_ip

    def merge(self, other):
        self.from_ip = min(self.from_ip, other.from_ip)
        self.to_ip = max(self.to_ip, other.to_ip)

    def __repr__(self):
        return str.format("[%d-%d]" % (self.from_ip, self.to_ip))

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(20)

    def reset(self):
        self.ranges = []

    def input_line(self, line):
        self.ranges.append(tuple(map(int, line.split('-'))))

    def solve1(self):
        ranges = self.create_ranges()
        first = ranges[0]
        if first.from_ip == 0:
            return str(first.to_ip)
        else:
            return '0'

    def solve2(self):
        ranges = self.create_ranges()
        valid = ranges[0].from_ip + MAX_IP - ranges[-1].to_ip
        for i in range(1, len(ranges)):
            valid += ranges[i].from_ip - ranges[i-1].to_ip
        return str(valid)

    def create_ranges(self):
        ranges = []
        # Sort ranges first on start ip: makes merging them quicker
        for a, b in sorted(self.ranges, key = lambda r: r[0]):
            r = ip_range(a, b + 1)
            self.add_and_reduce(r, ranges)
        ranges.sort(key = lambda r: r.from_ip)
        return ranges

    def add_and_reduce(self, r, ranges):
        changed = True
        while changed:
            changed = False
            to_remove = []
            for i, s in enumerate(ranges):
                if s.intersects(r):
                    r.merge(s)
                    changed = True
                    to_remove.append(i)
            for i in reversed(to_remove):
                del ranges[i]
        ranges.append(r)

r = runner()
r.run()
