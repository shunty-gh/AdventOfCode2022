import os
from collections import defaultdict

# https://adventofcode.com/2022/day/14 - Day 14: Regolith Reservoir

# Set either/both of these to true if you want to see the cave printed on the console.
# You'll need a console width of about 360 characters to show it properly for part 2
PRINT_CAVE_P1 = False
PRINT_CAVE_P2 = False

def build_cave(src: list[list[tuple[int,int]]]) -> dict[tuple[int,int], str]:
    result = defaultdict(lambda: '.')
    for coords in src:
        x0, y0 = coords[0]
        for i in range(1, len(coords)):
            x1, y1 = coords[i]
            my = 1 if y1 >= y0 else -1
            for y in range((my * (y1 - y0)) + 1):
                mx = 1 if x1 >= x0 else -1
                for x in range((mx * (x1 - x0)) + 1):
                    result[(x0+(mx*x),y0+(my*y))] = '#'
            x0,y0 = x1,y1

    return result

def find_next(map: dict[tuple[int,int],str], x: int, y: int) -> tuple[int,int] | None:
    # down; down left, down right
    if map[(x,y+1)] == '.':
        return (x,y+1)
    elif map[(x-1,y+1)] == '.':
        return (x-1,y+1)
    elif map[(x+1,y+1)] == '.':
        return (x+1,y+1)
    else:
        return None

def print_cave(cave: dict[tuple[int,int],str]):
    xmin = min([key[0] for key in cave.keys()])
    ymin = min([key[1] for key in cave.keys()])
    xmax = max([key[0] for key in cave.keys()])
    ymax = max([key[1] for key in cave.keys()])

    print('')
    for y in range(ymin-1, ymax):
        ln = ''
        for x in range(xmin-1, xmax+1):
            match cave[(x,y)]:
                case '.':
                    ln += ' '
                case 'o':
                    ln += '.'
                case '#':
                    ln += '#'
        print(ln)
    print("#" * (xmax-xmin+3))
    print("\n  You'll need at least", xmax-xmin+3, "character width to make this look right (and", ymax-ymin+3, "height to see it all)\n")

def pour_the_sand(cave: dict[tuple[int,int],str], is_part2: bool) -> int:
    maxdepth = max([key[1] for key in cave.keys()])
    if is_part2:
        maxdepth += 2
    origin: tuple[int,int] = (int(500), int(0))
    orgpath: list[tuple[int,int]] = []
    step = (origin, orgpath)
    while True:
        (x,y),path = step

        next = find_next(cave, x, y)
        if next == None or (is_part2 and next[1] == maxdepth):
            # reached the final resting point of this grain
            cave[(x,y)] = 'o'
            # if this is the origin then we've blocked the source and completed part 2
            if (x,y) == origin:
                break
            # trackback
            newpath = path.copy()
            prev = newpath.pop()
            step = (prev, newpath)
        elif next[1] >= maxdepth: # check if we've overflowed into the abyss (part 1 only)
            break
        else:
            newpath = path.copy()
            newpath.append((x,y))
            step = (next, newpath)

    if PRINT_CAVE_P1 and not is_part2:
        print_cave(cave)
    if PRINT_CAVE_P2 and is_part2:
        print_cave(cave)
    return sum([1 for c in cave.values() if c == 'o'])


#all_scans = [line.strip().split(' -> ') for line in "498,4 -> 498,6 -> 496,6\n503,4 -> 502,4 -> 502,9 -> 494,9".splitlines()]
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day14-input", "r") as f:
    all_scans = [line.strip().split(' -> ') for line in f.readlines()]
coords: list[list[tuple[int,int]]] = []
for scan in all_scans:
    coords.append(list(map(lambda s: (int(s.split(',')[0]), int(s.split(',')[1])), scan)))

print("Part 1: ", pour_the_sand(build_cave(coords), False))
print("Part 2: ", pour_the_sand(build_cave(coords), True))
