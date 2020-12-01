import math

def permutation_unique(list, length):
    if length == 1:
        return [(n,) for n in list]
    else:
        return [(list[i],) + v for i in range(len(list)) for v in permutation_unique(list[i+1:] , length -1)]


def puzzle(input, tuple_size, required_sum):
    permutation = permutation_unique([int(n) for n in input], tuple_size)
    matches = [t for t in permutation if sum(t) == required_sum]
    assert len(matches) == 1, f"We should have exactly one match for this puzzle. Got {matches}"
    return math.prod(matches[0])


def puzzle1(input):
    return puzzle(input, 2, 2020)

def puzzle2(input):
    return puzzle(input, 3, 2020)


assert puzzle1(['1721', '979', '366', '299', '675', '1456']) == 514579
assert puzzle2(['1721', '979', '366', '299', '675', '1456']) == 241861950

with open('input.txt') as f:
    print(f'The answer to part one is {puzzle1(f.readlines())}')
with open('input.txt') as f:
    print(f'The answer to part two is {puzzle2(f.readlines())}')

