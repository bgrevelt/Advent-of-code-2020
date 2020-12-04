import math

def isTree(map, x, y):
    mapWidth = len(map[0])
    x_index = x % mapWidth # map endlessly continues to the right.
    return map[y][x_index]


'''Translate input (lines containing "#" where there is a tree and "." where there is not
into a map. Which is really just a list of lists, e.g. a matrix'''
def inputToMap(input):
    return [[c == '#' for c in line] for line in input.split('\n')]

def count_trees(map, slope):
    numberOfTrees = 0
    x = 0
    y = 0
    while y < len(map):
        if isTree(map,x,y):
            numberOfTrees += 1

        x += slope[0]
        y += slope[1]

    return numberOfTrees

example_input = \
'''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''

assert count_trees(inputToMap(example_input), (3,1)) == 7

def puzzle1(input):
    return count_trees(inputToMap(puzzleInput), (3,1))

def puzzle2(input, slopes = [(1,1),(3,1),(5,1),(7,1),(1,2)]):
    map = inputToMap(input)
    treecCunts = [count_trees(map, slope) for slope in slopes]
    return math.prod(treecCunts)

assert puzzle2(example_input) == 336

puzzleInput = open('input.txt').read()
print(f'The answer to puzzle 1 is {puzzle1(puzzleInput)}')
print(f'The answer to puzzle 2 is {puzzle2(puzzleInput)}')
