import os
from collections import defaultdict, deque

# https://adventofcode.com/2022/day/14

def build_cave(src: list[list[tuple[int,int]]]) -> dict[tuple[int,int], str]:
    result = defaultdict(lambda: '.')
    for coord in src:
        x0, y0 = coord[0]
        for i in range(1, len(coord)):
            x1, y1 = coord[i]
            my = 1 if y1 >= y0 else -1
            for y in range((my * (y1 - y0)) + 1):
                mx = 1 if x1 >= x0 else -1
                for x in range((mx * (x1 - x0)) + 1):
                    result[(x0+(mx*x),y0+(my*y))] = '#'
            x0,y0 = x1,y1

    return result

def find_next(map, x, y):
    # down; down left, down right
    if map[(x,y+1)] == '.':
        return (x,y+1)
    elif map[(x-1,y+1)] == '.':
        return (x-1,y+1)
    elif map[(x+1,y+1)] == '.':
        return (x+1,y+1)
    else:
        return None


all_scans = [line.strip().split(' -> ') for line in "498,4 -> 498,6 -> 496,6\n503,4 -> 502,4 -> 502,9 -> 494,9".splitlines()]
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day14-input", "r") as f:
    all_scans = [line.strip().split(' -> ') for line in f.readlines()]
coords: list[list[tuple[int,int]]] = []
for scan in all_scans:
    coords.append(list(map(lambda s: (int(s.split(',')[0]), int(s.split(',')[1])), scan)))

cave = build_cave(coords)
maxdepth = max([key[1] for key in cave.keys()])
origin: tuple[int,int] = (int(500), int(0))
orgpath: list[tuple[int,int]] = []
q = deque([(origin, orgpath)])
while True:
    (x,y),path = q.pop()

    next = find_next(cave, x, y)
    if next == None:
        # reached the final resting point of this grain
        cave[(x,y)] = 'o'
        # trackback
        newpath = path.copy()
        prev = newpath.pop()
        q.append((prev, newpath))
    elif next[1] >= maxdepth: # check if we've overflowed into the abyss
        break
    else:
        newpath = path.copy()
        newpath.append((x,y))
        q.append((next, newpath))

print("Part 1: ", sum([1 for c in cave.values() if c == 'o']))
print("Part 2: ", )
