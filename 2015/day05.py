import adventofcode
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(5)

    def reset(self):
        self.strings = []

    def input_line(self, line):
        self.strings.append(line)

    def solve1(self):
        nice = 0
        for string in self.strings:
            if self.has_three_vowels(string) and self.has_duplication(string) and self.has_no_forbidden(string):
                nice += 1
        return str(nice)

    def has_three_vowels(self, string):
        vowels = {'a','e','i','o','u'}
        count = 0
        for c in string:
            if c in vowels:
                count += 1
        return count >= 3

    def has_duplication(self, string):
        last = ''
        for c in string:
            if c == last:
                return True
            last = c
        return False

    def has_no_forbidden(self, string):
        forbidden_regex = '(ab|cd|pq|xy)'
        return re.search(forbidden_regex, string) is None

    def solve2(self):
        nice = 0
        for string in self.strings:
            if self.has_xyx(string) and self.has_two_letter_duplication(string):
                nice += 1
        return str(nice)

    def has_xyx(self, string):
        max_len = len(string) - 2
        for i in range(max_len):
            if string[i] == string[i + 2]:
                return True
        return False

    def has_two_letter_duplication(self, string):
        max_len = len(string) - 1
        substrings = set()
        last = None
        for i in range(max_len):
            sub = string[i] + string[i + 1]
            if sub in substrings:
                return True
            substrings.add(last)
            last = sub
        return False

r = runner()

r.test('Sample 1', ['ugknbfddgicrmopn'], '1')
r.test('Sample 2', ['aaa'], '1')
r.test('Sample 3', ['jchzalrnumimnmhp'], '0')
r.test('Sample 4', ['haegwjzuvuyypxyu'], '0')
r.test('Sample 5', ['dvszwmarrgswjxmb'], '0')

r.test('Sample 2.1', ['qjhvhtzxzqqjkmpb'], None, '1')
r.test('Sample 2.2', ['xxyxx'], None, '1')
r.test('Sample 2.3', ['uurcxstgmygtbstg'], None, '0')
r.test('Sample 2.4', ['ieodomkazucvgmuy'], None, '0')

r.run()
