import adventofcode
import re

ORE = 'ORE'
FUEL = 'FUEL'

class element:
    def __init__(self, name, formula):
        self.name = name
        self.formula = formula
        self.needs = set()
        self.is_needed_for = set()
        self.amount_made = 0
        self.amount_needed = 0

    def clear(self):
        self.amount_made = 0
        self.amount_needed = 0

    def can_make(self):
        for x in self.is_needed_for:
            if x.amount_made == 0:
                # print('Cannot make %s: dependency %s not made' % (self.name, x.name))
                return False
        return True

    def make(self):
        amount_per_reaction = self.formula[self.name]
        multiplier = self.amount_needed // amount_per_reaction
        if self.amount_needed % amount_per_reaction > 0:
            multiplier += 1
        self.amount_made = amount_per_reaction * multiplier
        #print('Creating %d of %s (%d needed)' % (self.amount_made, self.name, self.amount_needed))
        for e in self.needs:
            e.amount_needed += multiplier * self.formula[e.name]

    def __repr__(self):
        return str.format('[%s: %d (%d)]' % (self.name, self.amount_made, self.amount_needed))

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(14)

    def reset(self):
        self.elements = dict()
        self.elements[ORE] = element(ORE, {ORE: 1})

    def input_line(self, line):
        formula = dict()
        for m in re.finditer(r'(\d+) ([A-Z]+)', line):
            formula[m.group(2)] = int(m.group(1))
            target_element = m.group(2)
        self.elements[target_element] = element(target_element, formula)

    def solve1(self):
        for name, e in self.elements.items():
            for x in e.formula.keys():
                if x != name:
                    self.elements[x].is_needed_for.add(e)
                    e.needs.add(self.elements[x])

        ore = self.chain_react(1)
        
        return str(ore.amount_needed)

    def solve2(self):
        ore_amount = 1000000000000

        min_fuel = ore_amount // self.elements[ORE].amount_needed
        max_fuel = min_fuel * 2

        while min_fuel < max_fuel - 1:
            new_fuel = (min_fuel + max_fuel) // 2
            if new_fuel == min_fuel:
                new_fuel += 1
            # print('Trying %d (%d-%d)' % (new_fuel, min_fuel, max_fuel))
            if self.chain_react(new_fuel).amount_needed <= ore_amount:
                min_fuel = new_fuel
            else:
                max_fuel = new_fuel

        return str(min_fuel)

    def chain_react(self, fuel_amount):
        for e in self.elements.values():
            e.clear()

        fuel = self.elements[FUEL]
        fuel.amount_needed = fuel_amount
        to_process = { fuel }
        while to_process:
            e = to_process.pop()
            e.make()
            for e2 in e.needs:
                if e2.can_make():
                    to_process.add(e2)
        return self.elements[ORE]

r = runner()

r.test('Sample last', [
    '171 ORE => 8 CNZTR',
    '7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL',
    '114 ORE => 4 BHXH',
    '14 VRPVC => 6 BMBT',
    '6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL',
    '6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT',
    '15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW',
    '13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW',
    '5 BMBT => 4 WPTQ',
    '189 ORE => 9 KTJDG',
    '1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP',
    '12 VRPVC, 27 CNZTR => 2 XDBXC',
    '15 KTJDG, 12 BHXH => 5 XCVML',
    '3 BHXH, 2 VRPVC => 7 MZWV',
    '121 ORE => 7 VRPVC',
    '7 XCVML => 6 RJRHP',
    '5 BHXH, 4 VRPVC => 5 LTCX',
], '2210736', '460664')

r.run()
