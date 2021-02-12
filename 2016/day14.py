import adventofcode
import hashlib
from collections import defaultdict

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(14)

    def reset(self):
        self.key = None

    def input_line(self, line):
        self.key = line

    def solve1(self):
        return str(self.find_64th_key(self.generate_hashes(self.key)))

    def solve2(self):
        return str(self.find_64th_key(self.generate_stretched_hashes(self.key)))

    def find_64th_key(self, generator):
        candidate_keys = defaultdict(list)
        keys = list()
        limit = 0
        for index, h in enumerate(generator):
            triple = self.get_triple(h)
            if triple:
                candidate_keys[triple].append(index)
            for c in self.get_quintuples(h):
                for candidate in candidate_keys[c]:
                    if candidate < index and index <= candidate + 1000:
                        print(candidate)
                        keys.append(candidate)
                        if len(keys) == 64:
                            # Check some more hashes because they _may_ result in smaller keys
                            limit = candidate + 1000
            if len(keys) >= 64 and index >= limit:
                break
        return sorted(keys)[63]

    def get_triple(self, h):
        prev = None
        count = 0
        for c in h:
            if c == prev:
                count += 1
                if count == 3:
                    return c
            else:
                count = 1
                prev = c
        return None

    def get_quintuples(self, h):
        result = set()
        prev = None
        count = 0
        for c in h:
            if c == prev:
                count += 1
                if count == 5:
                    result.add(c)
            else:
                count = 1
                prev = c
        return result

    def generate_hashes(self, key):
        number = 0
        while True:
            yield hashlib.md5((key + str(number)).encode('utf-8')).hexdigest()
            number += 1

    def generate_stretched_hashes(self, key):
        number = 0
        while True:
            val = hashlib.md5((key + str(number)).encode('utf-8')).hexdigest()
            for _ in range(2016):
                val = hashlib.md5(val.encode('utf-8')).hexdigest()
            yield val
            number += 1

r = runner()
r.run()
