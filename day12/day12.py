class Ship:
    def __init__(self):
        # direction in degrees/ North = 0, East = 90, south = 180, West = 270
        self._heading = 90
        self._northing = 0
        self._easting = 0

        self._actions = {
            'N' : self._move_north,
            'S' : self._move_south,
            'E' : self._move_east,
            'W' : self._move_west,
            'L' : self._rotate_left,
            'R' : self._rotate_right,
            'F' : self._move_forward
        }

    def take_action(self, instruction):
        action = instruction[0]
        value = int(instruction[1:])
        assert action in self._actions
        self._actions[action](value)

    def manhattan_distance(self):
        return abs(self._easting) + abs(self._northing)

    def _move_north(self, value):
        self._northing += value

    def _move_south(self, value):
        self._northing -= value

    def _move_east(self, value):
        self._easting += value

    def _move_west(self, value):
        self._easting -= value

    def _rotate_left(self, value):
        self._heading -= value
        self._heading %= 360 # make sure we stay on the 0-360 degree range
        assert self._heading % 90 == 0, 'Puzzle suggest that we should only point north, west, south, or east'

    def _rotate_right(self, value):
        self._heading += value
        self._heading %= 360  # make sure we stay on the 0-360 degree range
        assert self._heading % 90 == 0, 'Puzzle suggest that we should only point north, west, south, or east'

    def _move_forward(self, value):
        assert self._heading % 90 == 0, 'Puzzle suggest that we should only point north, west, south, or east'
        if self._heading == 0:
            self._move_north(value)
        elif self._heading == 90:
            self._move_east(value)
        elif self._heading == 180:
            self._move_south(value)
        else:
            assert self._heading == 270
            self._move_west(value)

s = Ship()
'''
F10
N3
F7
R90
F11
These instructions would be handled as follows:
'''
# F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
s.take_action('F10')
assert s._easting == 10
assert s._northing == 0
# N3 would move the ship 3 units north to east 10, north 3.
s.take_action('N3')
assert s._easting == 10
assert s._northing == 3
# F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
s.take_action('F7')
assert s._easting == 17
assert s._northing == 3
# R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
s.take_action('R90')
assert s._easting == 17
assert s._northing == 3
# F11 would move the ship 11 units south to east 17, south 8.
s.take_action('F11')
assert s._easting == 17
assert s._northing == -8
# At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.
assert s.manhattan_distance() == 25

def puzzle1(instructions):
    ship = Ship()
    for instruction in instructions:
        ship.take_action(instruction)
    return ship.manhattan_distance()

print(f'The solution to puzzle1 is {puzzle1(open("input.txt").readlines())}')

class ShipNew:
    def __init__(self):
        self._northing = 0
        self._easting = 0
        self._waypoint_northing = 1
        self._waypoint_easting = 10

        self._actions = {
            'N' : self._move_waypoint_north,
            'S' : self._move_waypoint_south,
            'E' : self._move_waypoint_east,
            'W' : self._move_waypoint_west,
            'L' : self._rotate_waypoint_left,
            'R' : self._rotate_waypoint_right,
            'F' : self._move_to_waypoint
        }

    def take_action(self, instruction):
        action = instruction[0]
        value = int(instruction[1:])
        assert action in self._actions
        self._actions[action](value)

    def manhattan_distance(self):
        return abs(self._easting) + abs(self._northing)

    def _move_waypoint_north(self, value):
        self._waypoint_northing += value

    def _move_waypoint_south(self, value):
        self._waypoint_northing -= value

    def _move_waypoint_east(self, value):
        self._waypoint_easting += value

    def _move_waypoint_west(self, value):
        self._waypoint_easting -= value

    def _rotate_waypoint_left(self, value):
        assert value % 90 == 0, 'puzzle suggests we only rotate a multitude of 90 degrees'
        for i in range(value // 90):
            self._rotate_90_degrees_waypoint_counter_clockwise()

    def _rotate_waypoint_right(self, value):
        assert value % 90 == 0, 'puzzle suggests we only rotate a multitude of 90 degrees'
        for i in range(value // 90):
            self._rotate_90_waypoint_degrees_clockwise()

    def _rotate_90_waypoint_degrees_clockwise(self):
        northing = -1 * self._waypoint_easting
        self._waypoint_easting = self._waypoint_northing
        self._waypoint_northing = northing

    def _rotate_90_degrees_waypoint_counter_clockwise(self):
        northing = self._waypoint_easting
        self._waypoint_easting = -1 * self._waypoint_northing
        self._waypoint_northing = northing

    def _move_to_waypoint(self, value):
        self._northing += self._waypoint_northing * value
        self._easting += self._waypoint_easting * value

# For example, using the same instructions as above:
s = ShipNew()
# F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
s.take_action('F10')
assert s._northing == 10
assert s._easting == 100
assert s._waypoint_northing == 1
assert s._waypoint_easting == 10
# N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
s.take_action('N3')
assert s._northing == 10
assert s._easting == 100
assert s._waypoint_northing == 4
assert s._waypoint_easting == 10
# F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
s.take_action('F7')
assert s._northing == 38
assert s._easting == 170
assert s._waypoint_northing == 4
assert s._waypoint_easting == 10
# R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
s.take_action('R90')
assert s._northing == 38
assert s._easting == 170
assert s._waypoint_northing == -10
assert s._waypoint_easting == 4

# F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
s.take_action('F11')
assert s._northing == -72
assert s._easting == 214
assert s._waypoint_northing == -10
assert s._waypoint_easting == 4
# After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.
assert s.manhattan_distance() == 286

def puzzle2(instructions):
    ship = ShipNew()
    for instruction in instructions:
        ship.take_action(instruction)
    return ship.manhattan_distance()

print(f'The solution to puzzle2 is {puzzle2(open("input.txt").readlines())}')