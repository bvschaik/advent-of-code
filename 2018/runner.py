import sys
import time

class runner:
    def solve(self):
        for line in sys.stdin:
            self.input(line)
        start = time.time()
        result1 = self.solve1()
        end1 = time.time()
        result2 = self.solve2()
        end2 = time.time()
        time1 = int((end1 - start) * 1000)
        time2 = int((end2 - end1) * 1000)
        print("Day %d: solution 1 = %s (%d ms), solution 2 = %s (%d ms)" % (self.day(), result1, time1, result2, time2))

    def day(self):
        return 0

    def input(self, line):
        pass

    def solve1(self):
        return ""

    def solve2(self):
        return ""
