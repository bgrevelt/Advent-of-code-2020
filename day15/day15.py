def reverse_find(numbers, n):
    # this creates a new (reversed) list. May be a bit slow, but let's see if it works
    numbers = numbers[::-1]
    return numbers.index(n)

def puzzle1(puzzle_input, stopat):
    numbers = {v : i for i,v in enumerate(puzzle_input[:-1])}
    turn = len(puzzle_input) - 1
    previous_number = puzzle_input[-1]
    while turn + 1 < stopat:
        # Then, each turn consists of considering the most recently spoken number:
        # If that was the first time the number has been spoken,
        if previous_number not in numbers:
            # the current player says 0.
            numbers[previous_number] = turn
            previous_number = 0
        else:
            # Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.
            distance = turn - numbers[previous_number]
            numbers[previous_number] = turn
            previous_number = distance

        turn += 1

    return previous_number

# Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be 436.
assert puzzle1([0,3,6],2020) == 436
# Given the starting numbers 1,3,2, the 2020th number spoken is 1.
assert puzzle1([1,3,2],2020) == 1
# Given the starting numbers 2,1,3, the 2020th number spoken is 10.
assert puzzle1([2,1,3],2020) == 10
# Given the starting numbers 1,2,3, the 2020th number spoken is 27.
assert puzzle1([1,2,3],2020) == 27
# Given the starting numbers 2,3,1, the 2020th number spoken is 78.
assert puzzle1([2,3,1],2020) == 78
# Given the starting numbers 3,2,1, the 2020th number spoken is 438.
assert puzzle1([3,2,1],2020) == 438
# Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
assert puzzle1([3,1,2],2020) == 1836

print(f'The solution to puzzle1 is {puzzle1([2,1,10,11,0,6],2020)}')

# Given 0,3,6, the 30000000th number spoken is 175594.
assert puzzle1([0,3,6],30000000) == 175594
# Given 1,3,2, the 30000000th number spoken is 2578.
assert puzzle1([1,3,2],30000000) == 2578
# Given 2,1,3, the 30000000th number spoken is 3544142.
assert puzzle1([2,1,3],30000000) == 3544142
# Given 1,2,3, the 30000000th number spoken is 261214.
assert puzzle1([1,2,3],30000000) == 261214
# Given 2,3,1, the 30000000th number spoken is 6895259.
assert puzzle1([2,3,1],30000000) == 6895259
# Given 3,2,1, the 30000000th number spoken is 18.
assert puzzle1([3,2,1],30000000) == 18
# Given 3,1,2, the 30000000th number spoken is 362.
assert puzzle1([3,1,2],30000000) == 362

print(f'The solution to puzzle2 is {puzzle1([2,1,10,11,0,6],30000000)}')