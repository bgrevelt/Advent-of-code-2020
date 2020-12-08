from collections import defaultdict

class Bag:
    def __init__(self, string):
        self.color = None
        self.can_contain = []
        self._processs_string(string)

    def __str__(self):
        s = f'{self.color} colored bag can contain\n'
        s += "\n".join([f'\t{count} {color} colored bags' for count, color in self.can_contain])
        return s


    def _processs_string(self, s):
        # format of input string is
        # <color> bags contain [N <color> bag(s)]+ | "No other bags".
        color, remainder = s.split('bags contain', 1)
        self.color = color.strip()
        for inner_bag in remainder.split(','):
            if "no other bags" in inner_bag:
                continue
            else:
                inner_bag = inner_bag.strip()
                count, remainder = inner_bag.split(' ', 1)
                color = remainder.replace('bags', '').replace('bag', '').replace('.','').strip()
                self.can_contain.append((int(count), color))

def to_containment_dict(input):
    can_be_contained_by = defaultdict(list)
    for line in input.splitlines():
        bag = Bag(line)
        for count, contained in bag.can_contain:
            can_be_contained_by[contained].append(bag.color)
    return can_be_contained_by

def to_tree(input):
    can_contain = defaultdict(list)
    bag_by_color = {}
    for line in input.splitlines():
        bag = Bag(line)
        bag_by_color[bag.color] = bag
        for count, color in bag.can_contain:
            can_contain[bag].append(color)




'''Returns all bag colors that can contain the provided bag color. Both direct and indirect'''
def get_containers(d, color):
    if color not in d or len(d[color]) == 0:
        return [color]
    else:
        return set([color] + [inner_color for outer_color in d[color] for inner_color in get_containers(d, outer_color)])

'''
rood -> 3 geel
geel -> 5 blauw

d = { rood : [3m ]
'''
def get_number_of_bags(d, color):
    if color not in d or len(d[color]) == 0:
        return 0
    else:
        return sum



test_input = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''

def puzzle1(puzzle_input):
    d = to_containment_dict(puzzle_input)
    containers = get_containers(d, 'shiny gold')
    containers.remove('shiny gold')
    return containers

containers = puzzle1(test_input)
'''In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.'''
assert len(containers) == 4
assert all(c in containers for c in ['bright white', 'muted yellow', 'dark orange', 'light red'])

print(f'The answer to puzzle1 is {len(puzzle1(open("input.txt").read()))}')



def to_containment_dict(input):
    can_be_contained_by = defaultdict(list)
    for line in input.splitlines():
        bag = Bag(line)
        can_be_contained_by[bag.color] = bag.can_contain
    return can_be_contained_by

def get_number_of_bags(d, color):
    if color not in d or len(d[color]) == 0:
        return 1
    else:
        return 1+ sum([count * get_number_of_bags(d, inner_color) for count, inner_color in d[color]])

def puzzle2(puzzle_input):
    return get_number_of_bags(to_containment_dict(puzzle_input), 'shiny gold') - 1

test_input = '''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.'''

assert puzzle2(test_input) == 126

print(f'The answer to puzzle2 is {puzzle2(open("input.txt").read())}')