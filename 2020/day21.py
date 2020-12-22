import adventofcode
import re

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(21)

    def reset(self):
        self.lines = []

    def input_line(self, line):
        m = re.match(r'(.*) \(contains (.*)\)', line)
        ingredients = set(m.group(1).split(' '))
        allergens = list(m.group(2).split(', '))
        self.lines.append((ingredients, allergens))

    def solve1(self):
        all_allergens = self.get_all_allergens()

        bad_ingredients = set()
        for ingredients in all_allergens.values():
            bad_ingredients.update(ingredients)

        return str(sum(map(lambda x: len(x[0] - bad_ingredients), self.lines)))

    def solve2(self):
        all_allergens = self.get_all_allergens()
        mapping = dict()
        changed = True
        while changed:
            changed = False
            for a in all_allergens:
                if len(all_allergens[a]) == 1:
                    ingredient = all_allergens[a].pop()
                    for b in all_allergens:
                        all_allergens[b].discard(ingredient)
                    mapping[a] = ingredient
                    changed = True
        return ','.join(map(lambda a: mapping[a], sorted(mapping.keys())))

    def get_all_allergens(self):
        all_allergens = dict()
        for (ingredients, allergens) in self.lines:
            for a in allergens:
                if a in all_allergens:
                    all_allergens[a] = all_allergens[a] & ingredients
                else:
                    all_allergens[a] = ingredients
        return all_allergens

r = runner()

r.test('Sample 1', [
    'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
    'trh fvjkl sbzzf mxmxvkd (contains dairy)',
    'sqjhc fvjkl (contains soy)',
    'sqjhc mxmxvkd sbzzf (contains fish)',
], '5', 'mxmxvkd,sqjhc,fvjkl')

r.run()
