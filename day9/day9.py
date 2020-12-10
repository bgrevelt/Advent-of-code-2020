'''
1,2,3,4
1,2
1,3
1,4
2,3
2,4
3,4

'''

def get_sums(numbers):
    return [numbers[left] + numbers[right] for left in range(len(numbers)) for right in range(left + 1, len(numbers))]


s = get_sums(list(range(1,26)))
# 26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
assert 26 in s
# 49 would be a valid next number, as it is the sum of 24 and 25.
assert 49 in s
# 100 would not be valid; no two of the previous 25 numbers sum to 100.
assert 100 not in s
# 50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.
assert 50 not in s

def puzzle1(numbers, preamble_size):
    numbers = [int(n) for n in numbers.splitlines()]
    for number_index in range(preamble_size, len(numbers)):
        number = numbers[number_index]
        preamble = numbers[number_index-preamble_size:number_index]
        sums = get_sums(preamble)
        if number not in sums:
            return number

test_input = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''

'''In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; 
the only number that does not follow this rule is 127.'''
assert puzzle1(test_input, 5) == 127

puzzle_input = open("input.txt").read()
result_puzzle1 = puzzle1(puzzle_input, 25)
print(f'The answer to puzzle1 is {result_puzzle1}')

def contiguous_sums(numbers, range_length):
    return [sum(numbers[n : n + range_length]) for n in range(0, len(numbers) - range_length)]

def puzzle2(numbers, requested_sum):
    numbers = [int(n) for n in numbers.splitlines()]
    for range_length in range(2, len(numbers) + 1):
        for number_range in [numbers[n : n + range_length] for n in range(0, len(numbers) - range_length)]:
            if sum(number_range) == requested_sum:
                return min(number_range) + max(number_range)

test_input = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''

# To find the encryption weakness, add together the smallest and largest number in this contiguous range;
# in this example, these are 15 and 47, producing 62.
assert puzzle2(test_input,127) == 62

print(f'The answer to puzzle2 is {puzzle2(puzzle_input, result_puzzle1)}')