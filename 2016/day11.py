import adventofcode
import re

GENERATOR = 0
MICROCHIP = 1
BOTTOM_FLOOR = 0
TOP_FLOOR = 3

class state_type:
    def __init__(self, elevator, pairs):
        self.elevator = elevator
        self.pairs = pairs

    def is_valid(self):
        for floor in range(4):
            has_generator = False
            has_unconnected_chip = False
            for pair in self.pairs:
                if pair[GENERATOR] == floor:
                    has_generator = True
                elif pair[1] == floor:
                    has_unconnected_chip = True
            if has_generator and has_unconnected_chip:
                return False
        return True

    def is_goal_state(self):
        return (self.elevator == TOP_FLOOR and
            all(map(lambda p: p[GENERATOR] == TOP_FLOOR and p[MICROCHIP] == TOP_FLOOR, self.pairs)))

    def all_moves(self):
        items_on_floor = [] # tuples: index of pair, type (generator or chip)
        for index, pair in enumerate(self.pairs):
            if pair[GENERATOR] == self.elevator:
                items_on_floor.append((index, GENERATOR))
            if pair[MICROCHIP] == self.elevator:
                items_on_floor.append((index, MICROCHIP))
        new_states = []
        directions = []
        if self.elevator != BOTTOM_FLOOR:
            directions.append(-1)
        if self.elevator != TOP_FLOOR:
            directions.append(1)
        for i in range(len(items_on_floor)):
            # Take only item i with us
            for d in directions:
                new_states.append(self.move_items(d, items_on_floor[i]))
            for j in range(i):
                # Take both i and j with us
                for d in directions:
                    new_states.append(self.move_items(d, items_on_floor[i], items_on_floor[j]))
        return new_states

    def move_items(self, delta, item1, item2 = None):
        new_pairs = list(self.pairs)
        index, item_type = item1
        if item_type == GENERATOR:
            new_pairs[index] = (self.pairs[index][0] + delta, self.pairs[index][1])
        else:
            new_pairs[index] = (self.pairs[index][0], self.pairs[index][1] + delta)
        if item2:
            index, item_type = item2
            if item_type == GENERATOR:
                new_pairs[index] = (self.pairs[index][0] + delta, self.pairs[index][1])
            else:
                new_pairs[index] = (self.pairs[index][0], self.pairs[index][1] + delta)
        return state_type(self.elevator + delta, new_pairs)

    def canonical(self):
        # It doesn't matter which pair is which for 'equivalent' states:
        # just sort 'em so we have a canonical representation
        return (self.elevator, tuple(sorted(self.pairs)))

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(11)

    def reset(self):
        self.items = dict()

    def input_line(self, line):
        if 'nothing relevant' in line:
            return
        m = re.match(r'The (.*) floor contains a (.*)\.', line)
        floor_names = ['first', 'second', 'third', 'fourth']
        floor = floor_names.index(m.group(1))
        items = m.group(2).replace(' and ', ', ').replace(',,', ',').split(', a ')
        print(m.group(2), items)
        for item in items:
            if item.endswith('microchip'):
                type_id = MICROCHIP
                type_name = item.split('-')[0]
            else:
                type_id = GENERATOR
                type_name = item.split(' ')[0]
            if type_name not in self.items:
                self.items[type_name] = [-1, -1]
            self.items[type_name][type_id] = floor

    def solve1(self):
        state = state_type(0, [])
        for generator, microchip in self.items.values():
            state.pairs.append((generator, microchip))

        return str(self.find_goal(state))

    def solve2(self):
        state = state_type(0, [])
        for generator, microchip in self.items.values():
            state.pairs.append((generator, microchip))
        state.pairs.append((0, 0)) # elerium
        state.pairs.append((0, 0)) # dilithium

        return str(self.find_goal(state))

    def find_goal(self, init_state):
        seen_states = set()
        states = [init_state]
        moves = 0
        while states:
            moves += 1
            # print('Move', moves, 'states', len(states))
            new_states = []
            for s in states:
                for ns in s.all_moves():
                    if ns.is_valid():
                        key = ns.canonical()
                        if key not in seen_states:
                            if ns.is_goal_state():
                                return moves
                            seen_states.add(key)
                            new_states.append(ns)
            states = new_states

r = runner()
r.run()
