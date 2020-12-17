def parse_input(text):
    r = {}
    z = 0
    for y, line in enumerate(text.splitlines()):
        for x, val in enumerate(line):
            r[(x,y,z)] = (val == '#')
    return r

def print_pocket_dimension(d):
    xs = {x for x,_,_ in d.keys()}
    ys = {y for _, y, _ in d.keys()}
    zs = {z for _,_,z in d.keys()}

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    for z in zs:
        print(f'Z={z}')

        for y in range(min_y,max_y+1):
            line = "".join("#" if (x,y,z) in d and d[(x,y,z)] else "." for x in range(min_x, max_x+1))
            print(line)
        print('\n')

def neighbours(cx,cy,cz):
    return [(x,y,z) for x in range(cx-1, cx+2) for y in range(cy-1, cy+2) for z in range(cz-1, cz+2) if not (cx == x and cy ==y and cz == z)]

def active_neighbours(cx,cy,cz, dimension):
    return [(x,y,z) for x,y,z in neighbours(cx,cy,cz) if (x,y,z) in dimension and dimension[(x,y,z)]]

def cycle(dimension):
    '''During a cycle, all cubes simultaneously change their state according to the following rules:
    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.'''
    dimension_copy = {k:v for k,v in dimension.items()}

    # Challenge here is that the dimension is infinite. That means we can't just look at the cubes we know about
    # Fortunately we know that all cubes we don't know about are inactive. And because something will only happen to a
    # cube if there are 2 or 3 active neighbours, we know we don't have to look further than 1 away from the known cubes
    xs = [x for x,_,_ in dimension.keys()]
    ys = [y for _, y, _ in dimension.keys()]
    zs = [z for _, _, z in dimension.keys()]
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)
    minz = min(zs)
    maxz = max(zs)

    for x in range(minx-1, maxx+2):
        for y in range(miny-1, maxy+2):
            for z in range(minz-1, maxz+2):
                #If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
                if (x,y,z) in dimension and dimension[(x,y,z)]:
                    if len(active_neighbours(x, y, z, dimension)) not in [2,3]:
                        dimension_copy[(x,y,z)] = False
                #If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
                elif len(active_neighbours(x, y, z, dimension)) == 3:
                        dimension_copy[(x,y,z)] = True
    return dimension_copy

def puzzle1(text):
    dim = parse_input(text)
    for n in range(6):
        dim = cycle(dim)
    return len([v for v in dim.values() if v])

print(f'The solution to puzzle 1 is {puzzle1(open("input.txt").read())}')