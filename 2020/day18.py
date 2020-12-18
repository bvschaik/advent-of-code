import adventofcode

NONE = 0
PLUS = 1
MULTIPLY = 2

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(18)

    def reset(self):
        self.calculations = []

    def input_line(self, line):
        self.calculations.append(line)

    def solve1(self):
        return str(sum(map(lambda x: self.calculate1(x), self.calculations)))

    def calculate1(self, line):
        stack = list()
        value = 0
        operator = NONE
        for c in line:
            if c == ' ':
                continue
            elif c == '+':
                operator = PLUS
            elif c == '*':
                operator = MULTIPLY
            elif c >= '0' and c <= '9':
                new_value = int(c)
                if operator == PLUS:
                    value += new_value
                elif operator == MULTIPLY:
                    value *= new_value
                else:
                    value = new_value
                operator = NONE
            elif c == '(':
                stack.append((value, operator))
                operator = NONE
                value = 0
            elif c == ')':
                (old_lhs, old_oper) = stack.pop()
                if old_oper == PLUS:
                    value += old_lhs
                elif old_oper == MULTIPLY:
                    value *= old_lhs
                operator = NONE
        return value

    def solve2(self):
        return str(sum(map(lambda x: self.calculate2(x), self.calculations)))

    def calculate2(self, line):
        stack = list()
        value = 0
        operator = NONE
        for c in line:
            if c == ' ':
                continue
            elif c == '+':
                operator = PLUS
            elif c == '*':
                stack.append((value, MULTIPLY, '*'))
                operator = NONE
                value = 0
            elif c >= '0' and c <= '9':
                new_value = int(c)
                if operator == PLUS:
                    value += new_value
                else:
                    value = new_value
                operator = NONE
            elif c == '(':
                stack.append((value, operator, '('))
                operator = NONE
                value = 0
            elif c == ')':
                value = self.pop_until_paren(stack, value)
        value = self.pop_until_paren(stack, value)
        return value

    def pop_until_paren(self, stack, value):
        until_seen = False
        while stack and not until_seen:
            (s_value, s_oper, push_val) = stack.pop()
            if s_oper == PLUS:
                value += s_value
            elif s_oper == MULTIPLY:
                value *= s_value
            until_seen = push_val == '('
        return value

r = runner()

r.test('Sample 1', ['1 + 2 * 3 + 4 * 5 + 6'], '71', '231')
r.test('Sample 2', ['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'], '13632', '23340')

r.run()
