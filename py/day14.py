import os
from collections import defaultdict

# https://adventofcode.com/2022/day/14 - Day 14: Regolith Reservoir

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

    return sum([1 for c in cave.values() if c == 'o'])


#all_scans = [line.strip().split(' -> ') for line in "498,4 -> 498,6 -> 496,6\n503,4 -> 502,4 -> 502,9 -> 494,9".splitlines()]
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day14-input", "r") as f:
    all_scans = [line.strip().split(' -> ') for line in f.readlines()]
coords: list[list[tuple[int,int]]] = []
for scan in all_scans:
    coords.append(list(map(lambda s: (int(s.split(',')[0]), int(s.split(',')[1])), scan)))

print("Part 1: ", pour_the_sand(build_cave(coords), False))
print("Part 2: ", pour_the_sand(build_cave(coords), True))
