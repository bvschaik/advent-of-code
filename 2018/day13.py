import adventofcode
import re

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

LEFT_DIR = [UP, RIGHT, DOWN, LEFT]
RIGHT_DIR = [DOWN, LEFT, UP, RIGHT]

class cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.intersect_count = 0
    
    def move(self):
        if self.direction == DOWN:
            self.y += 1
        elif self.direction == UP:
            self.y -= 1
        elif self.direction == LEFT:
            self.x -= 1
        else:
            self.x += 1

    def turn(self, new_direction):
        self.direction = new_direction
    
    def turn_intersection(self):
        if self.intersect_count == 0:
            self.direction = LEFT_DIR[self.direction]
        elif self.intersect_count == 2:
            self.direction = RIGHT_DIR[self.direction]
        self.intersect_count = (self.intersect_count + 1) % 3

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(13)

    def reset(self):
        self.carts = []
        self.map = []

    def input_line(self, line):
        y = len(self.map)
        self.map.append(line)
        for (x, c) in enumerate(line):
            if c == '^':
                self.carts.append(cart(x, y, UP))
            elif c == 'v':
                self.carts.append(cart(x, y, DOWN))
            elif c == '<':
                self.carts.append(cart(x, y, LEFT))
            elif c == '>':
                self.carts.append(cart(x, y, RIGHT))

    def solve1(self):
        my_carts = list()
        cart_positions = set()
        for c in self.carts:
            cart_positions.add((c.x, c.y))
            my_carts.append(cart(c.x, c.y, c.direction))
        while True:
            my_carts.sort(key = lambda c: (c.x, c.y))
            for c in my_carts:
                if not self.move_cart(c, cart_positions):
                    return str.format("%d,%d" % (c.x, c.y))
        pass

    def solve2(self):
        my_carts = list()
        cart_positions = set()
        for c in self.carts:
            cart_positions.add((c.x, c.y))
            my_carts.append(cart(c.x, c.y, c.direction))
        while True:
            my_carts.sort(key = lambda c: (c.x, c.y))
            for c in my_carts:
                if (c.x, c.y) in cart_positions:
                    if not self.move_cart(c, cart_positions):
                        cart_positions.remove((c.x, c.y))
                        my_carts = list(filter(lambda c2: c2.x != c.x or c2.y != c.y, my_carts))
            if len(my_carts) == 1:
                c = my_carts[0]
                return str.format("%d,%d" % (c.x, c.y))
        pass

    def move_cart(self, c, cart_positions):
        cart_positions.remove((c.x, c.y))
        c.move()
        new_pos = (c.x, c.y)
        if new_pos in cart_positions:
            return False
        cart_positions.add(new_pos)
        tile = self.map[c.y][c.x]
        if tile == '+':
            c.turn_intersection()
        elif tile == '/':
            if c.direction == RIGHT:
                c.turn(UP)
            elif c.direction == DOWN:
                c.turn(LEFT)
            elif c.direction == LEFT:
                c.turn(DOWN)
            elif c.direction == UP:
                c.turn(RIGHT)
        elif tile == '\\':
            if c.direction == LEFT:
                c.turn(UP)
            elif c.direction == DOWN:
                c.turn(RIGHT)
            elif c.direction == RIGHT:
                c.turn(DOWN)
            elif c.direction == UP:
                c.turn(LEFT)
        return True

r = runner()
r.test('Small circle', [
    "/--\\",
    "^  |",
    "\\->/"
], '3,0')

r.test('Sample input', [
    r"/->-\        ",
    r"|   |  /----\\",
    r"| /-+--+-\  |",
    r"| | |  | v  |",
    r"\-+-/  \-+--/",
    r"  \------/   "
], '7,3')

r.test('Sample input part 2', [
    '/>-<\\  ',
    '|   |  ',
    '| /<+-\\',
    '| | | v',
    '\\>+</ |',
    '  |   ^',
    '  \\<->/'
], '2,0', '6,4')

r.run()
