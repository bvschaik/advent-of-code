import adventofcode
import re

class cookie_props:
    def __init__(self, capacity, durability, flavor, texture, calories):
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def add(self, other, amount):
        return cookie_props(
            self.capacity + other.capacity * amount,
            self.durability + other.durability * amount,
            self.flavor + other.flavor * amount,
            self.texture + other.texture * amount,
            self.calories + other.calories * amount
        )

    def score(self):
        if self.capacity <= 0 or self.durability <= 0 or self.flavor <= 0 or self.texture <= 0:
            return 0
        return self.capacity * self.durability * self.flavor * self.texture

    def score_calories(self):
        if self.calories != 500:
            return 0
        else:
            return self.score()

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(15)

    def reset(self):
        self.ingredients = []

    def input_line(self, line):
        m = re.match(r'(.*): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line)
        name = m.group(1)
        capacity = int(m.group(2))
        durability = int(m.group(3))
        flavor = int(m.group(4))
        texture = int(m.group(5))
        calories = int(m.group(6))
        self.ingredients.append(cookie_props(capacity, durability, flavor, texture, calories))

    def solve1(self):
        score = self.combine_ingredients(self.ingredients, 100, cookie_props(0, 0, 0, 0, 0))
        return str(score)

    def combine_ingredients(self, ingredients, amount_left, stats):
        if len(ingredients) == 1:
            return stats.add(ingredients[0], amount_left).score()

        max_score = 0
        for n in range(amount_left + 1):
            new_stats = stats.add(ingredients[-1], n)
            score = self.combine_ingredients(ingredients[0:-1], amount_left - n, new_stats)
            if score > max_score:
                max_score = score
        return max_score

    def solve2(self):
        score = self.combine_ingredients_calories(self.ingredients, 100, cookie_props(0, 0, 0, 0, 0))
        return str(score)

    def combine_ingredients_calories(self, ingredients, amount_left, stats):
        if len(ingredients) == 1:
            return stats.add(ingredients[0], amount_left).score_calories()

        max_score = 0
        for n in range(amount_left + 1):
            new_stats = stats.add(ingredients[-1], n)
            if new_stats.calories > 500:
                continue
            score = self.combine_ingredients_calories(ingredients[0:-1], amount_left - n, new_stats)
            if score > max_score:
                max_score = score
        return max_score


r = runner()

r.test('Sample', [
    'Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8',
    'Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3',
], '62842880', '57600000')

r.run()
