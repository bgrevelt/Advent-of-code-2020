def validate_password(password, requiredchar, min, max):
    assert len(requiredchar) == 1, "Should be a single character"
    count = password.count(requiredchar)
    return min <= count <= max

def validate_password_alt(password, required_char, pos1, pos2):
    index1 = pos1 - 1 # 1-based to 0-based
    index2 = pos2 - 1
    return (password[index1] == required_char) != (password[index2] == required_char) # poor man's exor

def parse_input(line):
    ''' format:
     <min>-<max> <required character>: <password>'''
    assert len(line) > 7, f'line {line} does not conform to the expected format'

    count, required, password = line.split(' ')
    min, max = count.split('-')
    min = int(min)
    max = int(max)
    required = required[0]

    return min,max,required,password

def validate_line(line, validate_function):
    min, max, required, password = parse_input(line)
    return validate_function(password, required, min, max)

def puzzle1(lines):
    return len([line for line in lines if validate_line(line, validate_password)])

def puzzle2(lines):
    return len([line for line in lines if validate_line(line, validate_password_alt)])

assert validate_line('1-3 a: abcde', validate_password) == True
assert validate_line('1-3 b: cdefg', validate_password) == False
assert validate_line('2-9 c: ccccccccc', validate_password) == True
assert puzzle1(['1-3 a: abcde','1-3 b: cdefg','2-9 c: ccccccccc']) == 2

assert validate_line('1-3 a: abcde', validate_password_alt) == True
assert validate_line('1-3 b: cdefg', validate_password_alt) == False
assert validate_line('2-9 c: ccccccccc', validate_password_alt) == False
assert puzzle2(['1-3 a: abcde','1-3 b: cdefg','2-9 c: ccccccccc']) == 1


with open('input.txt') as f:
    lines = f.readlines()
    print(f'The answer to puzzle 1 is {puzzle1(lines)}')
    print(f'The answer to puzzle 2 is {puzzle2(lines)}')