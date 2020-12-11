class SeatLayout:
    def __init__(self, text):
        # x and y reversed. E,g, _seats[y][x]
        self._seats = [[c for c in row] for row in text.splitlines()]
        self._dimy = len(self._seats)
        self._dimx = len(self._seats[0]) if self._dimy > 0 else 0

    def get_occupied(self,x,y):
        return self._seats[y][x] == '#'

    def get_empty(self, x, y):
        return self._seats[y][x] == 'L'

    def set_occupied(self, x, y):
        self._seats[y][x] = '#'

    def set_empty(self, x, y):
        self._seats[y][x] = 'L'

    def is_seat(self, x, y):
        return self._seats[y][x] != '.'

    def get_total_occupied(self):
        sum = 0
        for x,y in self.seats():
            if self.get_occupied(x,y):
                sum += 1
        return sum

    def get_occupied_adjecent_seats(self, x, y):
        count = 0
        for x,y in self._get_adjacent_seats(x,y):
            if self.get_occupied(x,y):
                count += 1
        return count

    def seats(self):
        for x in range(self._dimx):
            for y in range(self._dimy):
                yield x,y

    def _get_adjacent_seats(self, x, y):
        start_x = x-1 if x >0 else 0
        start_y = y-1 if y > 0 else 0
        end_x = min(x+1, self._dimx -1)
        end_y = min(y+1, self._dimy -1)

        return [(ix,iy) for ix in range(start_x, end_x + 1) for iy in range(start_y, end_y + 1) if not (ix == x and iy == y)]

    def get_occupied_visible_seats(self, x, y):
        count = 0
        for x, y in self._get_directly_visible_seats(x, y):
            if self.get_occupied(x, y):
                count += 1
        return count

    def _get_directly_visible_seats(self, x, y):
        seats = []
        directions = [(-1,-1), (-1,0), (-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        for dx, dy in directions:
            for steps in range(1,max(self._dimy, self._dimx)):
                nx = x + dx * steps
                ny = y + dy * steps
                if nx >= 0 and nx < self._dimx and ny >= 0 and ny < self._dimy:
                    if self.is_seat(nx, ny):
                        seats.append((nx,ny))
                        break
                else:
                    # Out of bounds. No seat in this direction
                    break
        return seats

    def apply_model(self):
        new_seats = SeatLayout(str(self))
        for x,y in self.seats():
            # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if self.get_empty(x,y) and self.get_occupied_adjecent_seats(x,y) == 0:
                new_seats.set_occupied(x,y)
            # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            elif self.get_occupied(x,y) and self.get_occupied_adjecent_seats(x,y) >= 4:
                new_seats.set_empty(x, y)
            # Otherwise, the seat's state does not change.
        self._seats = new_seats._seats

    def apply_model2(self):
        new_seats = SeatLayout(str(self))
        for x, y in self.seats():
            if self.get_empty(x, y) and self.get_occupied_visible_seats(x, y) == 0:
                new_seats.set_occupied(x, y)
            elif self.get_occupied(x, y) and self.get_occupied_visible_seats(x, y) >= 5:
                new_seats.set_empty(x, y)
        self._seats = new_seats._seats


    def __str__(self):
        return "\n".join([''.join(row) for row in self._seats])

example_input = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''
example_layout = SeatLayout(example_input)

example_layout.apply_model()

'''After one round of these rules, every seat in the example layout becomes occupied:
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##'''

assert str(example_layout) == '''#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##'''

'''After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##'''

example_layout.apply_model()
assert str(example_layout) == '''#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##'''

'''This process continues for three more rounds:'''

example_layout.apply_model()
assert str(example_layout) == '''#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##'''

example_layout.apply_model()
assert str(example_layout) == '''#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##'''

example_layout.apply_model()
assert str(example_layout) == '''#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##'''

def puzzle1(input):
    previous = input
    layout = SeatLayout(input)
    while True:
        layout.apply_model()
        current = str(layout)
        if current == previous:
            break
        else:
            previous = current
    return layout.get_total_occupied()

# Once people stop moving around, you count 37 occupied seats.
assert puzzle1(example_input) == 37

print(f'The solution to puzzle1 is {puzzle1(open("input.txt").read())}')

example_layout = SeatLayout(example_input)
example_layout.apply_model2()
assert str(example_layout) == '''#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##'''

example_layout.apply_model2()
assert str(example_layout) == '''#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#'''

example_layout.apply_model2()
assert str(example_layout) == '''#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#'''

example_layout.apply_model2()
assert str(example_layout) == '''#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#'''

example_layout.apply_model2()
assert str(example_layout) == '''#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#'''

example_layout.apply_model2()
assert str(example_layout) == '''#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#'''


def puzzle2(input):
    previous = input
    layout = SeatLayout(input)
    while True:
        layout.apply_model2()
        current = str(layout)
        if current == previous:
            break
        else:
            previous = current
    return layout.get_total_occupied()

assert puzzle2(example_input) == 26

print(f'The solution to puzzle2 is {puzzle2(open("input.txt").read())}')