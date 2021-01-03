import adventofcode

class match_data:
    def __init__(self, sequence):
        self.sequence = sequence
        self.num_matches = 0

    def matches(self, number):
        if self.sequence[self.num_matches] == number:
            self.num_matches += 1
            if self.num_matches == len(self.sequence):
                return True
        else:
            self.num_matches = 0
        return False

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(14)

    def reset(self):
        self.input_recipe = 0

    def input_line(self, line):
        self.input_recipe = line

    def solve1(self):
        max_recipes = int(self.input_recipe)

        recipes = [3, 7]
        elf1 = 0
        elf2 = 1
        while len(recipes) < max_recipes + 10:
            new_recipes = recipes[elf1] + recipes[elf2]
            if (new_recipes >= 10):
                recipes.append(new_recipes // 10)
                recipes.append(new_recipes % 10)
            else:
                recipes.append(new_recipes)
            elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
            elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)

        return ''.join(map(lambda x: str(x), recipes[max_recipes:max_recipes+10]))

    def solve2(self):
        sequence = list(map(lambda c: int(c), self.input_recipe))
        matcher = match_data(sequence)

        recipes = [3, 7]
        elf1 = 0
        elf2 = 1
        found = False
        while not found:
            new_recipes = recipes[elf1] + recipes[elf2]
            if (new_recipes >= 10):
                value1 = new_recipes // 10
                recipes.append(value1)
                if matcher.matches(value1):
                    return str(len(recipes) - len(sequence))
                value2 = new_recipes % 10
                recipes.append(value2)
                if matcher.matches(value2):
                    return str(len(recipes) - len(sequence))
            else:
                recipes.append(new_recipes)
                if matcher.matches(new_recipes):
                    return str(len(recipes) - len(sequence))
            elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
            elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
        pass

r = runner()
r.test('Sample 1', ['9'], '5158916779')
r.test('Sample 2', ['5'], '0124515891')
r.test('Sample 5', ['2018'], '5941429882')

r.test('Sample 2.1', ['51589'], '3910137144', '9')
r.test('Sample 2.5', ['59414'], '5131221087', '2018')

r.run()
