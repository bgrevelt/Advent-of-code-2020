def binary_partition(data, upper):
    if upper:
        return data[len(data) // 2 :]
    else:
        return data[:len(data) // 2 :]

def get_id(row, column):
    return row * 8 + column

def get_seat_id(input):
    row_count = 128
    column_count = 8

    input = input.strip()
    assert len(input) == 10

    rows = list(range(row_count))
    columns = list(range(column_count))
    for dir in input[:7]:
        rows = binary_partition(rows, dir == "B")
    for dir in input[7:]:
        columns = binary_partition(columns, dir == "R")

    assert len(rows) == 1, "We should end up with a single row"
    assert len(columns) == 1, "We should end up with a single column"

    return get_id(rows[0], columns[0])

# In this example, the seat has ID 44 * 8 + 5 = 357.
assert get_seat_id('FBFBBFFRLR') == 357
# BFFFBBFRRR: row 70, column 7, seat ID 567.
assert get_seat_id('BFFFBBFRRR') == 567
# FFFBBBFRRR: row 14, column 7, seat ID 119.
assert get_seat_id('FFFBBBFRRR') == 119
# BBFFBBFRLL: row 102, column 4, seat ID 820.
assert get_seat_id('BBFFBBFRLL') == 820

def puzzle1(puzzle_input):
    return max(get_seat_id(seat) for seat in puzzle_input)

def puzzle2(puzzle_input):
    all_seats_ids = {get_id(row, column) for row in range(127) for column in range(8)}
    boarding_pass_seat_ids = {get_seat_id(seat) for seat in puzzle_input}
    missing_seat_ids = all_seats_ids - boarding_pass_seat_ids
    for missing_seat_id in missing_seat_ids:
        if missing_seat_id -1 in boarding_pass_seat_ids and missing_seat_id + 1 in boarding_pass_seat_ids:
            return missing_seat_id

puzzle_input = open('input.txt').readlines()
print(f'The solution to puzzle 1 is {puzzle1(puzzle_input)}')
print(f'The solution to puzzle 2 is {puzzle2(puzzle_input)}')