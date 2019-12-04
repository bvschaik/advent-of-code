import adventofcode

INFINITE = 100000000

class wire_segment_horizontal:
    def __init__(self, x1, x2, y, direction, total_length):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.direction = direction
        self.total_length = total_length

    def length_to(self, x):
        if self.direction < 0:
            return self.total_length + self.x2 - x
        else:
            return self.total_length + x - self.x1

    def __repr__(self):
        return str.format('H(x = %d..%d, y = %d)' % (self.x1, self.x2, self.y))

class wire_segment_vertical:
    def __init__(self, x, y1, y2, direction, total_length):
        self.x = x
        self.y1 = y1
        self.y2 = y2
        self.direction = direction
        self.total_length = total_length

    def length_to(self, y):
        if self.direction < 0:
            return self.total_length + self.y2 - y
        else:
            return self.total_length + y - self.y1

    def __repr__(self):
        return str.format('V(x = %d, y = %d..%d)' % (self.x, self.y1, self.y2))

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(3)

    def reset(self):
        self.wires = []

    def input_line(self, line):
        self.wires.append(list(line.split(',')))

    def solve1(self):
        (wire1_horizontal, wire1_vertical) = self.parse_wire(self.wires[0])
        (wire2_horizontal, wire2_vertical) = self.parse_wire(self.wires[1])

        min_intersection = INFINITE
        for h in wire1_horizontal:
            for v in wire2_vertical:
                if self.intersects(h, v):
                    intersection = abs(v.x) + abs(h.y)
                    if intersection > 0 and intersection < min_intersection:
                        min_intersection = intersection

        for h in wire2_horizontal:
            for v in wire1_vertical:
                if self.intersects(h, v):
                    intersection = abs(v.x) + abs(h.y)
                    if intersection > 0 and intersection < min_intersection:
                        min_intersection = intersection

        return str(min_intersection)

    def solve2(self):
        (wire1_horizontal, wire1_vertical) = self.parse_wire(self.wires[0])
        (wire2_horizontal, wire2_vertical) = self.parse_wire(self.wires[1])

        min_length = INFINITE
        for h in wire1_horizontal:
            for v in wire2_vertical:
                if self.intersects(h, v):
                    length = h.length_to(v.x) + v.length_to(h.y)
                    if length > 0 and length < min_length:
                        min_length = length

        for h in wire2_horizontal:
            for v in wire1_vertical:
                if self.intersects(h, v):
                    length = h.length_to(v.x) + v.length_to(h.y)
                    if length > 0 and length < min_length:
                        min_length = length

        return str(min_length)

    def parse_wire(self, segments):
        x = 0
        y = 0
        total_length = 0

        horizontal_wires = []
        vertical_wires = []
        for s in segments:
            length = int(s[1:])
            if s[0] == 'R':
                horizontal_wires.append(wire_segment_horizontal(x, x + length, y, 1, total_length))
                x += length
            elif s[0] == 'L':
                horizontal_wires.append(wire_segment_horizontal(x - length, x, y, -1, total_length))
                x -= length
            elif s[0] == 'D':
                vertical_wires.append(wire_segment_vertical(x, y, y + length, 1, total_length))
                y += length
            elif s[0] == 'U':
                vertical_wires.append(wire_segment_vertical(x, y - length, y, -1, total_length))
                y -= length
            total_length += length

        return (horizontal_wires, vertical_wires)

    def intersects(self, wire_horiz, wire_vert):
        return (wire_horiz.x1 <= wire_vert.x and wire_vert.x <= wire_horiz.x2 and
            wire_vert.y1 <= wire_horiz.y and wire_horiz.y <= wire_vert.y2)

r = runner()

r.test('Sample input', [
    'R8,U5,L5,D3',
    'U7,R6,D4,L4'
], '6', '30')

r.run()
