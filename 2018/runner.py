import sys
import time

class runner:
    def solve(self):
        for line in sys.stdin:
            self.input(line.rstrip())
        start = time.time()
        result1 = self.solve1()
        end1 = time.time()
        result2 = self.solve2()
        end2 = time.time()
        time1 = int((end1 - start) * 1000)
        time2 = int((end2 - end1) * 1000)
        print("Day %d: solution 1 = %s (%d ms), solution 2 = %s (%d ms)" % (self.day(), result1, time1, result2, time2))

    def test(self, name, inputs, expected1, expected2 = None):
        print("Running test:", name)
        for line in inputs:
            self.input(line)
        result1 = self.solve1()
        if result1 == expected1:
            print("Solution 1: OK")
        else:
            print("Solution 1: NOK, expected '%s' but got '%s'" % (expected1, result1))
        if expected2 != None:
            result2 = self.solve2()
            if result2 == expected2:
                print("Solution 2: OK")
            else:
                print("Solution 2: NOK, expected '%s' but got '%s'" % (expected2, result2))

    def day(self):
        return 0

    def input(self, line):
        pass

    def solve1(self):
        return ""

    def solve2(self):
        return ""
