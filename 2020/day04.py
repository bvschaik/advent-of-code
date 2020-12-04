import adventofcode
import re

class passport_type:
    def __init__(self):
        self.props = dict()

    def add(self, key, value):
        self.props[key] = value

    def has_all_fields(self):
        keys = set(self.props.keys())
        required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
        return len(required - keys) == 0

    def is_valid(self):
        if not self.has_all_fields():
            return False
        return (
            self.is_valid_year(self.props['byr'], 1920, 2002) and
            self.is_valid_year(self.props['iyr'], 2010, 2020) and
            self.is_valid_year(self.props['eyr'], 2020, 2030) and
            self.is_valid_color(self.props['hcl']) and
            self.is_valid_eye(self.props['ecl']) and
            self.is_valid_height(self.props['hgt']) and
            self.is_valid_passport(self.props['pid'])
        )

    def is_valid_year(self, year, min_value, max_value):
        return re.match(r'^\d{4}$', year) is not None and int(year) >= min_value and int(year) <= max_value

    def is_valid_color(self, color):
        return re.match(r'^#[a-f0-9]{6}$', color) is not None
    
    def is_valid_height(self, height):
        m = re.match(r'^(\d+)(cm|in)$', height)
        if not m:
            return False
        value = int(m.group(1))
        if m.group(2) == 'cm':
            return value >= 150 and value <= 193
        else:
            return value >= 59 and value <= 76

    def is_valid_eye(self, eye):
        return re.match(r'^(amb|blu|brn|gry|grn|hzl|oth)$', eye) is not None

    def is_valid_passport(self, passport):
        return re.match(r'^\d{9}$', passport) is not None

class runner(adventofcode.runner):
    def __init__(self):
        super().__init__(4)

    def reset(self):
        self.passports = [passport_type()]

    def input_line(self, line):
        if len(line) == 0:
            self.passports.append(passport_type())
        else:
            passport = self.passports[len(self.passports) - 1]
            for part in line.split():
                (key, value) = part.split(':')
                passport.add(key, value)

    def solve1(self):
        return str(sum(map(lambda p: p.has_all_fields(), self.passports)))

    def solve2(self):
        return str(sum(map(lambda p: p.is_valid(), self.passports)))

r = runner()

r.test('Sample 1', [
    'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
    'byr:1937 iyr:2017 cid:147 hgt:183cm',
    '',
    'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
    'hcl:#cfa07d byr:1929',
    '',
    'hcl:#ae17e1 iyr:2013',
    'eyr:2024',
    'ecl:brn pid:760753108 byr:1931',
    'hgt:179cm',
    '',
    'hcl:#cfa07d eyr:2025 pid:166559648',
    'iyr:2011 ecl:brn hgt:59in',
], '2', '1')

r.run()
