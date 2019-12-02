import sys
import time

class runner:
    def __init__(self, day):
        self.day = day

    def run(self):
        self.reset()
        if len(sys.argv) > 1 and sys.argv[1] != 'skip-test':
            filepath = sys.argv[1]
        else:
            filepath = str.format("input/%02d.txt" % (self.day))
        with open(filepath) as fp:
            for line in fp:
                self.input_line(line.rstrip())
        print("Day %d:" % (self.day))
        start = time.time()
        result1 = self.solve1()
        end = time.time()
        time1 = int((end - start) * 1000)
        print("Solution 1: %s (%d ms)" % (result1, time1))
        start = time.time()
        result2 = self.solve2()
        end = time.time()
        time2 = int((end - start) * 1000)
        if result2:
            print("Solution 2: %s (%d ms)" % (result2, time2))

    def test(self, name, lines, expected1, expected2 = None):
        if len(sys.argv) > 1 and sys.argv[1] == 'skip-test':
            return
        self.reset()
        print(name, end = ' ')
        for line in lines:
            self.input_line(line)
        if expected1:
            result1 = self.solve1()
            if result1 == expected1:
                print("OK", end = '')
            else:
                print("NOK: expected [%s] actual [%s]" % (expected1, result1), end = '')
        if expected2:
            result2 = self.solve2()
            if result2 == expected2:
                print("OK")
            else:
                print("NOK: expected [%s] actual [%s]" % (expected2, result2))
        else:
            print()

    def reset(self):
        pass

    def input_line(self, line):
        pass

    def solve1(self):
        return ''

    def solve2(self):
        return ''
