import adventofcode
import copy
import re

type_immune = 0
type_infection = 1

class attack_group:
    def __init__(self, type, id, units, hitpoints, attack, attack_type, initiative, modifiers):
        self.type = type
        self.id = id
        self.units = units
        self.hitpoints = hitpoints
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative
        self.modifiers = modifiers
        self.target = None

    def __repr__(self):
        mods = str(self.modifiers)
        return str.format("attack_group(t=%d, u=%d, hp=%d, a=%d %s, init=%d, mods=" % (
            self.type, self.units, self.hitpoints, self.attack, self.attack_type, self.initiative)) + mods + ')'

    def damage_modifier(self, attack_type):
        return self.modifiers[attack_type] if attack_type in self.modifiers else 1

    def copy(self):
        return copy.copy(self)

    def copy_with_boost(self, boost):
        c = copy.copy(self)
        c.attack += boost
        return c

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(24)

    def reset(self):
        self.immune_system = []
        self.infection = []
        self.current = type_immune

    def input_line(self, line):
        if not line:
            return
        if line == 'Immune System:':
            self.current = type_immune
        elif line == 'Infection:':
            self.current = type_infection
        else:
            m = re.match(r'(\d+) units each with (\d+) hit points \(?([^)]*)\)? ?with an attack that does (\d+) (.*) damage at initiative (\d+)', line)
            modifiers_line = m.group(3)
            weaknesses = re.search(r'weak to ([^;]+)', modifiers_line)
            modifiers = dict()
            if weaknesses:
                for w in weaknesses.group(1).split(', '):
                    modifiers[w] = 2
            immunities = re.search(r'immune to ([^;]+)', modifiers_line)
            if immunities:
                for i in immunities.group(1).split(', '):
                    modifiers[i] = 0
            army = self.immune_system if self.current == type_immune else self.infection
            army.append(attack_group(self.current, len(army) + 1, int(m.group(1)), int(m.group(2)), int(m.group(4)), m.group(5), int(m.group(6)), modifiers))

    def solve1(self):
        all_armies = [copy.copy(x) for x in self.infection] + [copy.copy(x) for x in self.immune_system]
        winning_army = self.do_battle(all_armies)

        return str(sum(map(lambda a: a.units, winning_army)))

    def solve2(self):
        min_boost = 1
        max_boost = 100
        while min_boost < max_boost:
            boost = min_boost + (max_boost - min_boost) // 2
            all_armies = [x.copy_with_boost(boost) for x in self.immune_system] + [x.copy() for x in self.infection]
            winning_army = self.do_battle(all_armies)
            if winning_army and winning_army[0].type == type_immune:
                max_boost = boost
            else:
                min_boost = boost + 1
        boost = min_boost
        all_armies = [x.copy_with_boost(boost) for x in self.immune_system] + [x.copy() for x in self.infection]
        winning_army = self.do_battle(all_armies)
        return str(sum(map(lambda a: a.units, winning_army)))

    def do_battle(self, all_armies):
        can_continue = True
        play_round = 1
        while can_continue:
            all_armies.sort(key = lambda a: (a.units * a.attack, a.initiative), reverse = True)

            # Target selection phase
            targets = list(all_armies)
            for army in all_armies:
                target_groups = list(filter(lambda x: x.type != army.type, targets))
                target_groups.sort(key = lambda x: (x.damage_modifier(army.attack_type), x.units * x.attack, x.initiative), reverse = True)
                if target_groups and target_groups[0].damage_modifier(army.attack_type) > 0:
                    target = target_groups[0]
                    targets.remove(target)
                    army.target = target
                else:
                    army.target = None

            # Attack phase
            all_armies.sort(key = lambda a: a.initiative, reverse = True)
            total_killed = 0
            for army in all_armies:
                target = army.target
                if target and army.units > 0:
                    total_damage = army.units * army.attack * target.damage_modifier(army.attack_type)
                    killed_units = total_damage // target.hitpoints
                    target.units -= killed_units
                    total_killed += killed_units

            all_armies = list(filter(lambda a: a.units > 0, all_armies))
            can_continue = len(set(map(lambda a: a.type, all_armies))) > 1
            if can_continue and total_killed == 0:
                return None

        return all_armies

r = runner()
r.test('Sample input', [
    'Immune System:',
    '17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2',
    '989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3',
    '',
    'Infection:',
    '801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1',
    '4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4',
], '5216')

r.run()
