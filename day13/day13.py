import math
import datetime

def get_first_bus(time_to_leave, ids):
    ids = [int(id) for id in ids if id != 'x']
    wait_times = [id - (time_to_leave % id) for id in ids]
    min_wait_time = min(wait_times)
    return min_wait_time, ids[wait_times.index(min_wait_time)]

def puzzle1(puzzle_input):
    time_to_leave, schedule = puzzle_input.splitlines()
    time_to_leave = int(time_to_leave)
    schedule = schedule.split(',')
    wait_time, id = get_first_bus(time_to_leave, schedule)
    return wait_time * id

assert puzzle1('''939
7,13,x,x,59,x,31,19''') == 295

print(f'The solution to puzzle1 is {puzzle1(open("input.txt").read())}')


'''Phew, this took me a long time to get right. Let's try to explain what I did. I started with the naive implementation; 
go through all natural numbers and try to find one for which all((t + delay) % id == 0 for delay, id in input). That worked
fine for the example, but didn't scale well. So I started thinking about a faster solution. When we have all of these
delay combinations we end up with a set of equations with a whole bunch of unknowns:
t = <ID1> * A
t = <ID2> * B - 1
t = <ID3> * C - 4
...

or
<ID1> * A = <ID2> * B - 1 <ID3> * C - 4


And all we really know is that A, B, and C are natural numbers. 
There is probably a proper mathematical way of solving an equation like this, but I'm not very smart, so I thought of my
own solution. Here it is:

In the example given before, we know that the only values for B that we need to evaluate are those where B + 1 is a
multitude of <ID1> otherwise the first equation wouldn't match. Taking that further, the only values that we need to evaluate 
for C are those for which the first two equations match. 

Fortunately, there is a pattern for when two equations match. For example, let's say <ID1> is 5 and <ID2> is 3:

----*----*----*----*----*----*----*----*----*----*----*----*----*
--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
    ^              ^              ^              ^
    t=5            t=20           t-35           t=50            t=65

We see the first match at t = 5, the second at t=20, the third at t=35 and so on. In other words, we can replace
t = 5 * A
and
t = 3 * B + 1
with
t= 15 * X + 5

Now we can do the same trick for t = 15X + 5 = <ID3> + C + d and on and on until we are left with a single equation in
the form
t = a + N * X where a is the first time where all equations match. E.g. the solution to the puzzle 
'''


def find_match(start1, increment1, start2, increment2, startxat = 0):
    '''
    Find the first value for t for which there are some natural number for N and M where
    t = <start1> + N * <increment1> = <start1> + M * <increment2> holds where N >= <startxat>

    return that 't'
    '''

    x = startxat
    y = 0
    while True:
        resultx = start1 + x * increment1
        resulty = start2 + y * increment2
        if resultx == resulty:
            return start1 +  increment1 * x
        elif resultx < resulty:
            x = math.ceil((resulty - start1) / increment1)
        else:
            y = math.ceil((resultx - start2) / increment2)

def reduce_schedule(schedule):
    '''
    The schedule is a list of (delay, interval) tuples
    Reduce takes the first two of these and combines them to one as explained in the big comment on top. Then
    returns the reduced list
    '''
    if len(schedule) < 2:
        return schedule

    delayx = schedule[0][0]
    incrementx = schedule[0][1]
    delayy = schedule[1][0]
    incrementy = schedule[1][1]

    first_match = find_match(delayx, incrementx, delayy, incrementy)
    second_match = find_match(delayx, incrementx, delayy, incrementy, first_match // incrementx + 1)

    start = first_match
    increment = second_match - first_match

    schedule = [(start, increment)] + schedule[2:]
    return schedule


def puzzle2(puzzle_input):
    _, schedule = puzzle_input.splitlines()
    schedule = [(-1 * inx, int(id)) for inx, id in enumerate(schedule.split(',')) if id != 'x']

    '''
    Reduce the schedule until we only have one entry left. The first t where all busses leave on the
    desired time is the 'delay' of that one entry (and the situation repears every 'increment', but 
    no one cares about that'''
    while len(schedule) > 1:
        schedule = reduce_schedule(schedule)

    return schedule[0][0]


print(f'The solution to puzzle2 is {puzzle2(open("input.txt").read())}')