import adventofcode

class item_type:
    def __init__(self, cost, damage, armor):
        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __repr__(self):
        return str.format("[%d %d %d]" % (self.cost, self.damage, self.armor))

class unit_type:
    def __init__(self, hp, damage = 0, armor = 0):
        self.hp = hp
        self.damage = damage
        self.armor = armor
        self.cost = 0
        self.min_cost = 100000
        self.max_cost = 0

    def equip(self, item):
        self.cost += item.cost
        self.damage += item.damage
        self.armor += item.armor

    def unequip(self, item):
        self.cost -= item.cost
        self.damage -= item.damage
        self.armor -= item.armor

    def do_battle(self, enemy):
        if self.defeats(enemy):
            if self.cost < self.min_cost:
                self.min_cost = self.cost
        else:
            if self.cost > self.max_cost:
                self.max_cost = self.cost

    def defeats(self, enemy):
        self_attack = self.damage - enemy.armor
        if self_attack <= 0: self_attack = 1
        enemy_attack = enemy.damage - self.armor
        if enemy_attack <= 0: enemy_attack = 1
        turns_to_survive = self.hp // enemy_attack
        turns_to_kill = enemy.hp // self_attack
        if enemy.hp % self_attack > 0:
            turns_to_kill += 1
        return turns_to_survive + 1 >= turns_to_kill

WEAPONS = [
    item_type(8, 4, 0),
    item_type(10, 5, 0),
    item_type(25, 6, 0),
    item_type(40, 7, 0),
    item_type(74, 8, 0),
]

ARMOR = [
    item_type(13, 0, 1),
    item_type(31, 0, 2),
    item_type(53, 0, 3),
    item_type(75, 0, 4),
    item_type(102, 0, 5),
]

RINGS = [
    item_type(25, 1, 0),
    item_type(50, 2, 0),
    item_type(100, 3, 0),
    item_type(20, 0, 1),
    item_type(40, 0, 2),
    item_type(80, 0, 3),
]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(21)

    def reset(self):
        self.boss_hp = 0
        self.boss_damage = 0
        self.boss_armor = 0

    def input_line(self, line):
        parts = line.split(':')
        value = int(parts[1].strip())
        if parts[0] == 'Hit Points':
            self.boss_hp = value
        elif parts[0] == 'Damage':
            self.boss_damage = value
        elif parts[0] == 'Armor':
            self.boss_armor = value

    def solve1(self):
        self.boss = unit_type(self.boss_hp, self.boss_damage, self.boss_armor)
        self.player = unit_type(100)
        self.choose_weapon(self.player)
        return str(self.player.min_cost)

    def choose_weapon(self, player):
        for w in WEAPONS:
            player.equip(w)
            self.choose_armor(player)
            player.unequip(w)

    def choose_armor(self, player):
        # No armor
        self.choose_rings(player)
        for a in ARMOR:
            player.equip(a)
            self.choose_rings(player)
            player.unequip(a)

    def choose_rings(self, player):
        boss = self.boss
        # No rings
        player.do_battle(boss)
        max_rings = len(RINGS)
        for r1 in range(max_rings - 1):
            player.equip(RINGS[r1])
            player.do_battle(boss) # One ring
            for r2 in range(r1 + 1, max_rings):
                player.equip(RINGS[r2])
                player.do_battle(boss)
                player.unequip(RINGS[r2])
            player.unequip(RINGS[r1])

    def solve2(self):
        return str(self.player.max_cost)

r = runner()
r.run()
