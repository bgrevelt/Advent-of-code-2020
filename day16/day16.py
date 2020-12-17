import math

class Rule:
    def __init__(self, name, ranges):
        self.name = name
        self.ranges = ranges

    def numbers_valid(self, numbers):
        return all(self.number_valid(number) for number in numbers)

    def number_valid(self, value):
        return any(start <= value <= end for start, end in self.ranges)

    def __str__(self):
        ranges = ", ".join([f'[{start}-{end}]' for start,end in self.ranges])
        return f'{self.name}: {ranges}'

class Input:
    def __init__(self, text):
        self.your_ticket = None
        self.nearby_tickets = []
        self.rules = []

        state = 'rules'
        for line in text.splitlines():
            if line.startswith('your ticket'):
                state = 'your ticket'
            elif line.startswith('nearby tickets'):
                state = 'nearby tickets'
            elif line.strip():
                if state == 'rules':
                    self.rules.append(self._parse_rule(line))
                elif state == 'your ticket':
                    self.your_ticket = self._parse_ticket(line)
                elif state == 'nearby tickets':
                    self.nearby_tickets.append(self._parse_ticket(line))
                else:
                    assert False, "Uknown state"

    def valid_tickets(self):
        return [ticket for ticket in self.nearby_tickets if all(any(rule.number_valid(number) for rule in self.rules)for number in ticket )]

    def valid_numers(self):
        # returns a list of lists: [[number1 ticket1, number1 ticket2,..., number1 ticketN],...,[numberN ticket1, numberN ticket2,..., numberN ticketN]]
        assert len(set([len(ticket) for ticket in self.valid_tickets()])) == 1, "All tickets should have the same length"

        tickets = self.valid_tickets()
        return [[ticket[i] for ticket in tickets] for i in range(len(tickets[0]))]

    def matched_rules(self, values):
        return [rule for rule in self.rules if rule.numbers_valid(values)]

    def invalid_numbers(self):
        invalid_numbers = []
        for ticket in self.nearby_tickets:
            for number in ticket:
                if not any(rule.number_valid(number) for rule in self.rules):
                    invalid_numbers.append(number)
        return invalid_numbers

    def _parse_ticket(self, line):
        return [int(n) for n in line.strip().split(',')]

    def _parse_rule(self, line):
        name, rest = line.split(':')
        ranges = []
        for range in rest.split(' or '):
            range = range.strip()
            start,end = range.split('-')
            ranges.append((int(start), int(end)))
        return Rule(name, ranges)


test_input = '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12'''

def puzzle1(text):
    parsed = Input(text)
    return sum(parsed.invalid_numbers())

assert puzzle1(test_input) == 71

print(f'The solution to puzzle 1 is {puzzle1(open("input.txt").read())}')

'''
When we match the numbers to rules we end up with some number matching multiple rules. There should also be values that
only match a single rule. If that's the case we know that that rule has to match those values (or we did something wrong)
That also means that rule is no longer an option for other values, so we can take those out of set of matched rules.
That's what this function does at it continues doing so until every set of values matches a single rule. 
'''
def reduce_matches(matches):
    while any(len(m) > 1 for m in matches.values()):
        singularly_matched = [match[0] for match in matches.values() if len(match) == 1]
        matches = {i : [v for v in values if len(values) == 1 or v not in singularly_matched] for i, values in matches.items()}

    return {i: match[0] for i, match in matches.items()}

def puzzle2(text):
    parsed = Input(text)
    valid_numbers = parsed.valid_numers()
    matches_by_index = {i : parsed.matched_rules(values) for i, values in enumerate(valid_numbers)}
    matches_by_index= reduce_matches(matches_by_index)

    indexes_of_interest = [i for i, rule in matches_by_index.items() if rule.name.startswith('departure')]
    values_of_interest = [v for i,v in enumerate(parsed.your_ticket) if i in indexes_of_interest]
    return math.prod(values_of_interest)

print(f'The solution to puzzle 2 is {puzzle2(open("input.txt").read())}')