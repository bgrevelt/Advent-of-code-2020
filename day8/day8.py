class Processor:
    def __init__(self, input):
        self._operations = []
        self._accumulator = 0
        self._program_counter = 0
        self.pc_trace = []
        self._properly_terminated = False

        for line in input:
            operation, argument = line.split(' ')
            argument = int(argument)
            self._operations.append((operation, argument))

    def run(self):
        while self._program_counter < len(self._operations):
            self.pc_trace.append(self._program_counter)

            operation, argument = self._operations[self._program_counter]
            if operation == 'acc':
                self._accumulator += argument
                self._program_counter += 1
            elif operation == 'jmp':
                self._program_counter += argument
            elif operation == 'nop':
                self._program_counter += 1
            else:
                assert False, f'Unsupported instruction {operation}'

            if self._program_counter == len(self._operations):
                self._properly_terminated = True
                break

            if self._program_counter in self.pc_trace:
                break

    def accumulator(self):
        return self._accumulator

    def properly_terminated(self):
        return self._properly_terminated

test_input = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''

p = Processor(test_input.splitlines())
p.run()
'''Immediately before the program would run an instruction a second time, the value in the accumulator is 5.'''
assert p.accumulator() == 5

puzzle_input = open('input.txt').readlines()
p = Processor(puzzle_input)
p.run()
print(f'The solution to puzzle1 is {p.accumulator()}')

def change_operation(operations, index):
    operation = operations[index][:3]
    if operation == 'jmp':
        operations[index] = 'nop' + operations[index][3:]
    elif operation == 'nop':
        operations[index] = 'jmp' + operations[index][3:]

def puzzle2(puzzle_input):
    for change_index in range(len(puzzle_input)):
        input_copy = [l for l in puzzle_input]
        operation = puzzle_input[change_index][:3]
        if operation == 'acc':
            continue
        elif operation == 'jmp':
            input_copy[change_index] = 'nop' + input_copy[change_index][3:]
        elif operation == 'nop':
            input_copy[change_index] = 'jmp' + input_copy[change_index][3:]

        p = Processor(input_copy)
        p.run()
        if p.properly_terminated():
            return p.accumulator()

print(f'The solution to puzzle2 is {puzzle2(puzzle_input)}')