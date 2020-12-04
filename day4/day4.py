import re

class Passport:
    def __init__(self, text):
        self._required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
        self._fields = {}
        for keyValuePair in text.split(): # a little dodgy because this will split on any whitespace. I'm banking on the input not containing any tabs
            key, value = keyValuePair.split(':')
            self._fields[key] = value

    def isValid(self, strict = False, ):
        if strict:
            return self._strict_validation()
        else:
            return self._lax_validation()

    def _lax_validation(self):
        return all(required_field in self._fields.keys() for required_field in self._required_fields)

    def _strict_validation(self):
        # first make sure all the needed fields are there
        if not self._lax_validation():
            return False
        return all(self._validateField(field, value) for field, value in self._fields.items() if field in self._required_fields)

    def _validateField(self, key, value):
        if key == 'byr':
            #byr (Birth Year) - four digits; at least 1920 and at most 2002.
            return len(value) == 4 and self._validate_number(value, 1920, 2002)
        elif key == 'iyr':
            #iyr (Issue Year) - four digits; at least 2010 and at most 2020.
            return len(value) == 4 and self._validate_number(value, 2010, 2020)
        elif key == 'eyr':
            # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
            return len(value) == 4 and self._validate_number(value, 2020, 2030)
        elif key == 'hgt':
            return self._validate_height(value)
        elif key == 'hcl':
            # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
            return len(value) == 7 and re.match('#[0-9a-f]{6}', value) is not None
        elif key == 'ecl':
            # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
            return value in ['amb','blu','brn','gry','grn','hzl','oth']
        elif key == 'pid':
            # pid (Passport ID) - a nine-digit number, including leading zeroes.
            return len(value) == 9 and re.match('[0-9]{9}', value) is not None
        else:
            assert False, f"Uknown key {key}"

    def _validate_number(self, value, min, max):
        return min <= int(value) <= max

    def _validate_height(self, value):
        # hgt (Height) - a number followed by either cm or in:
        unit = value[-2:]
        if unit not in ["in", "cm"]:
            return False

        if unit == 'cm':
            # If cm, the number must be at least 150 and at most 193.
            return self._validate_number(value[:-2], 150, 193)
        else:
            # If in, the number must be at least 59 and at most 76.
            return self._validate_number(value[:-2], 59, 76)

    def __str__(self):
        return f'{str(self._fields)}\t{"Valid" if self.isValid() else "Invalid"}'

def parse_input(input):
    return [Passport(passportText) for passportText in input.split('\n\n')]

example_input = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''

def puzzle1(text):
    passports = parse_input(text)
    return len([passport for passport in passports if passport.isValid()])

assert puzzle1(example_input) == 2

p = Passport('')
# byr valid:   2002
assert p._validateField('byr', '2002')
# byr invalid: 2003
assert p._validateField('byr', '2003') == False
# hgt valid:   60in
assert p._validateField('hgt', '60in')
# hgt valid:   190cm
assert p._validateField('hgt', '190cm')
# hgt invalid: 190in
assert p._validateField('hgt', '190in') == False
# hgt invalid: 190
assert p._validateField('hgt', '190') == False
# hcl valid:   #123abc
assert p._validateField('hcl', '#123abc')
# hcl invalid: #123abz
assert p._validateField('hcl', '#123abz') == False
# hcl invalid: 123abc
assert p._validateField('hcl', '123abc') == False
# ecl valid:   brn
assert p._validateField('ecl', 'brn')
# ecl invalid: wat
assert p._validateField('ecl', 'wat') == False
# pid valid:   000000001
assert p._validateField('pid', '000000001')
# pid invalid: 0123456789
assert p._validateField('pid', '0123456789') == False

# Here are some invalid passports:
#
# eyr:1972 cid:100
# hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
assert Passport('''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926''').isValid(strict=True) == False
# iyr:2019
# hcl:#602927 eyr:1967 hgt:170cm
# ecl:grn pid:012533040 byr:1946
assert Passport('''iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946''').isValid(strict=True) == False
# hcl:dab227 iyr:2012
# ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
assert Passport('''hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277''').isValid(strict=True) == False
# hgt:59cm ecl:zzz
# eyr:2038 hcl:74454a iyr:2023
# pid:3556412378 byr:2007
assert Passport('''hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007''').isValid(strict=True) == False

# Here are some valid passports:
# pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
# hcl:#623a2f
assert Passport('''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f''').isValid(strict=True)
# eyr:2029 ecl:blu cid:129 byr:1989
# iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
assert Passport('''eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm''').isValid(strict=True)
# hcl:#888785
# hgt:164cm byr:2001 iyr:2015 cid:88
# pid:545766238 ecl:hzl
# eyr:2022
assert Passport('''hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022''').isValid(strict=True)
# iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
assert Passport('''iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719''').isValid(strict=True)

def puzzle2(text):
    passports = parse_input(text)
    return len([passport for passport in passports if passport.isValid(strict=True)])

puzzle_input = open('input.txt').read()
print(f'The answer to puzzle one is {puzzle1(puzzle_input)}')
print(f'The answer to puzzle two is {puzzle2(puzzle_input)}')