import adventofcode

class spell_type:
    def __init__(self, name, cost, effect_turns = 0):
        self.name = name
        self.cost = cost
        self.effect_turns = effect_turns

    def apply_immediate(self, game):
        pass

    def apply_effect(self, game):
        pass

class magic_missile(spell_type):
    def __init__(self):
        super().__init__('Magic Missile', 53)

    def apply_immediate(self, game):
        game.boss_hp -= 4

class drain(spell_type):
    def __init__(self):
        super().__init__('Drain', 73)

    def apply_immediate(self, game):
        game.player_hp += 2
        game.boss_hp -= 2

class shield(spell_type):
    def __init__(self):
        super().__init__('Shield', 113, 6)

    def apply_effect(self, game):
        game.player_armor += 7

class poison(spell_type):
    def __init__(self):
        super().__init__('Poison', 173, 6)

    def apply_effect(self, game):
        game.boss_hp -= 3

class recharge(spell_type):
    def __init__(self):
        super().__init__('Recharge', 229, 5)

    def apply_effect(self, game):
        game.player_mana += 101

PLAYER = 1
BOSS = 2

class game_state:
    def __init__(self,
            boss_hp, boss_attack,
            player_hp = 50, player_mana = 500, mana_spent = 0,
            player_armor = 0, active_effects = dict()):
        self.boss_hp = boss_hp
        self.boss_attack = boss_attack
        self.player_hp = player_hp
        self.player_mana = player_mana
        self.mana_spent = mana_spent
        self.player_armor = player_armor
        self.active_effects = dict(active_effects)
        self.winner = None

    def cast(self, spell, difficulty):
        if self.player_mana < spell.cost:
            return None
        if spell.name in self.active_effects:
            return None
        new_state = game_state(
            self.boss_hp, self.boss_attack,
            self.player_hp, self.player_mana - spell.cost, self.mana_spent + spell.cost,
            self.player_armor, self.active_effects
        )
        spell.apply_immediate(new_state)
        if spell.effect_turns:
            new_state.active_effects[spell.name] = (spell, spell.effect_turns)
        # Boss turn
        new_state.apply_effects()
        new_state.boss_turn()
        if new_state.player_hp <= 0:
            new_state.winner = BOSS
        # Start of next turn
        new_state.player_hp -= difficulty
        if difficulty and new_state.player_hp <= 0:
            new_state.winner = BOSS
        new_state.apply_effects()
        if new_state.boss_hp <= 0:
            new_state.winner = PLAYER
        return new_state

    def apply_effects(self):
        self.player_armor = 0
        to_remove = []
        for key in self.active_effects:
            (effect, time) = self.active_effects[key]
            effect.apply_effect(self)
            if time == 1:
                to_remove.append(key)
            else:
                self.active_effects[key] = (effect, time - 1)
        for key in to_remove:
            del self.active_effects[key]

    def boss_turn(self):
        attack = self.boss_attack - self.player_armor
        if attack < 1: attack = 1
        self.player_hp -= attack

    def is_finished(self):
        return self.boss_hp <= 0 or self.player_hp <= 0

    def is_won(self):
        return self.winner == PLAYER

    def __repr__(self):
        return str.format("Boss hp %d, player hp %d, armor %d, mana %d" %
            (self.boss_hp, self.player_hp, self.player_armor, self.player_mana))

ALL_SPELLS = [
    magic_missile(),
    drain(),
    shield(),
    poison(),
    recharge()
]

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(22)

    def reset(self):
        self.boss_hp = 0
        self.boss_damage = 0

    def input_line(self, line):
        parts = line.split(':')
        value = int(parts[1].strip())
        if parts[0] == 'Hit Points':
            self.boss_hp = value
        elif parts[0] == 'Damage':
            self.boss_damage = value

    def solve1(self):
        game = game_state(self.boss_hp, self.boss_damage)
        self.min_mana = 1000000
        self.recurse(game)
        return str(self.min_mana)

    def solve2(self):
        game = game_state(self.boss_hp, self.boss_damage, 49)
        self.min_mana = 1000000
        self.recurse(game, 1)
        return str(self.min_mana)

    def recurse(self, game, difficulty = 0):
        if game.is_finished():
            if game.is_won() and game.mana_spent < self.min_mana:
                self.min_mana = game.mana_spent
            return
        if game.mana_spent > self.min_mana:
            return
        for spell in ALL_SPELLS:
            new_game = game.cast(spell, difficulty)
            if new_game:
                self.recurse(new_game, difficulty)

r = runner()
r.run()
