import adventofcode

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(7)

    def reset(self):
        self.programs = dict()

    def input_line(self, line):
        parts = line.split(' -> ')
        if len(parts) > 1:
            upper = parts[1].split(', ')
        else:
            upper = []
        (name, weight) = parts[0].split(' (')
        self.programs[name] = (int(weight[0:-1]), upper)

    def solve1(self):
        lower_programs = set(self.programs.keys())
        for weight, upper in self.programs.values():
            for p in upper:
                lower_programs.discard(p)
        self.root_program = lower_programs.pop()
        return self.root_program

    def solve2(self):
        self.corrected_weight = None
        self.get_weights(self.root_program)
        return str(self.corrected_weight)

    def get_weights(self, root):
        (weight, upper) = self.programs[root]
        if upper:
            upper_weights = list(map(lambda p: self.get_weights(p), upper))
            weights = dict()
            for i, w in enumerate(upper_weights):
                if w in weights:
                    right_weight = w
                    weights[w].append(upper[i])
                else:
                    weights[w] = [upper[i]]
            if len(weights) > 1 and not self.corrected_weight:
                for w in weights:
                    if len(weights[w]) == 1:
                        wrong_weight = w
                        wrong_program = weights[w][0]
                        self.corrected_weight = right_weight - wrong_weight + self.programs[wrong_program][0]
            return weight + sum(upper_weights)
        else:
            return weight
        

r = runner()

r.test('Sample 2', [
    'pbga (66)',
    'xhth (57)',
    'ebii (61)',
    'havc (66)',
    'ktlj (57)',
    'fwft (72) -> ktlj, cntj, xhth',
    'qoyq (66)',
    'padx (45) -> pbga, havc, qoyq',
    'tknk (41) -> ugml, padx, fwft',
    'jptl (61)',
    'ugml (68) -> gyxo, ebii, jptl',
    'gyxo (61)',
    'cntj (57)',
], 'tknk', '60')

r.run()
