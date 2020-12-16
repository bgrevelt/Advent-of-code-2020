def process_instructions(lines):
    set_mask = 0
    clear_mask = 0
    memory = {}
    for line in lines:
        if line.startswith('mask'):
            mask = line[7:]
            set_mask = int(mask.replace('X', '0'), 2)  # for setting bits, set Xs to zero
            clear_mask = int(mask.replace('X', '1'), 2)  # for clearing bits, set Xs to 1
        else:
            assert line.startswith('mem[')
            address = int(line.split('[')[1].split(']')[0])
            value = int(line.split('=')[1])
            value |= set_mask
            value &= clear_mask
            memory[address] = value
    return memory

def puzzle1(lines):
    mem = process_instructions(lines)
    return sum(mem.values())


result = process_instructions('''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''.splitlines())

assert 8 in result
assert 7 in result
assert result[7] == 101
assert result[8] == 64

assert puzzle1('''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''.splitlines()) == 165

print(f'The solution to puzzle 1 is {puzzle1(open("input.txt").readlines())}')


def set_bit(value, bit):
    return value | 2**bit

def clear_bit(value, bit):
    mask = (2**bit) ^ (2**36-1)
    return value & mask

def boolean_permutation(values):
    r = []
    for n in range(2**len(values)):
        line = []
        for i, val in enumerate(values):
            bool = (n // 2**i) % 2 == 1
            line.append((val, bool))
        r.append(line)
    return r


def apply_mask(address, mask):
    floating_bits = [len(mask) - i -1 for i, v in enumerate(mask) if v == 'X']

    set_mask = int(mask.replace('X', '0'),2)
    address |= set_mask

    addresses = []
    for set in boolean_permutation(floating_bits):
        new_address = address
        for bit, value in set:
            if value:
                new_address = set_bit(new_address, bit)
            else:
                new_address = clear_bit(new_address, bit)
        addresses.append(new_address)
    return addresses

assert sorted(apply_mask(42, '000000000000000000000000000000X1001X')) == [26,27,58,59]
assert sorted(apply_mask(26, '00000000000000000000000000000000X0XX')) == [16,17,18,19,24,25,26,27]

def process_instructions2(lines):
    memory = {}
    for line in lines:
        if line.startswith('mask'):
            mask = line[7:].strip()
        else:
            assert line.startswith('mem[')
            address = int(line.split('[')[1].split(']')[0])
            value = int(line.split('=')[1])
            for floating_address in apply_mask(address, mask):
                memory[floating_address] = value
    return memory

def puzzle2(lines):
    mem = process_instructions2(lines)
    return sum(mem.values())

assert puzzle2('''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1'''.splitlines()) == 208

print(f'The solution to puzzle 2 is {puzzle2(open("input.txt").readlines())}')

