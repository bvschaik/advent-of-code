import adventofcode
import re

INPUT_FIELDS = 0
INPUT_MY_TICKET = 1
INPUT_TICKETS = 2

class field_type:
    def __init__(self, name, start1, end1, start2, end2):
        self.name = name
        self.range1 = (start1, end1)
        self.range2 = (start2, end2)
        self.index = -1

    def is_in_range(self, n):
        return (n >= self.range1[0] and n <= self.range1[1]) or (n >= self.range2[0] and n <= self.range2[1])

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(16)

    def reset(self):
        self.input_type = INPUT_FIELDS
        self.fields = []
        self.my_ticket = None
        self.nearby_tickets = []

    def input_line(self, line):
        if not line:
            self.input_type += 1
        elif self.input_type == INPUT_FIELDS:
            m = re.match(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', line)
            self.fields.append(field_type(m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))))
        elif self.input_type == INPUT_MY_TICKET:
            if line != 'your ticket:':
                self.my_ticket = list(map(int, line.split(',')))
        elif self.input_type == INPUT_TICKETS:
            if line != 'nearby tickets:':
                self.nearby_tickets.append(list(map(int, line.split(','))))

    def solve1(self):
        invalid = sum(map(lambda t: self.get_invalid_number(t), self.nearby_tickets))
        return str(invalid)

    def get_invalid_number(self, ticket):
        invalid_numbers = 0
        for n in ticket:
            matches = False
            for field in self.fields:
                if field.is_in_range(n):
                    matches = True
                    break
            if not matches:
                invalid_numbers += n
        return invalid_numbers

    def solve2(self):
        max_fields = len(self.my_ticket)
        tickets = self.get_valid_tickets()
        fields = dict(map(lambda f: (f.name, f), self.fields))
        options = []
        for i in range(len(self.my_ticket)):
            options.append(set(map(lambda f: f.name, self.fields)))

        # Remove impossible fields from the options at each index
        for i in range(max_fields):
            to_remove = set()
            for f in options[i]:
                for t in tickets:
                    if not fields[f].is_in_range(t[i]):
                        to_remove.add(f)
            options[i].difference_update(to_remove)

        # Repeatedly find the index with only 1 option, fill it in, remove it from the other indices
        changed = True
        while changed:
            changed = False
            for i in range(max_fields):
                if len(options[i]) == 1:
                    f = options[i].pop()
                    fields[f].index = i
                    for n in range(max_fields):
                        options[n].discard(f)
                    changed = True

        # Find the result
        result = 1
        for f in fields:
            if f.startswith('departure'):
                result *= self.my_ticket[fields[f].index]
        return str(result)

    def get_valid_tickets(self):
        tickets = []
        for ticket in self.nearby_tickets:
            valid = True
            for n in ticket:
                matches = False
                for field in self.fields:
                    if field.is_in_range(n):
                        matches = True
                        break
                if not matches:
                    valid = False
                    break
            if valid:
                tickets.append(ticket)
        return tickets

r = runner()

r.test('Sample 1', [
    'class: 1-3 or 5-7',
    'row: 6-11 or 33-44',
    'seat: 13-40 or 45-50',
    '',
    'your ticket:',
    '7,1,14',
    '',
    'nearby tickets:',
    '7,3,47',
    '40,4,50',
    '55,2,20',
    '38,6,12',
], '71')

r.run()
