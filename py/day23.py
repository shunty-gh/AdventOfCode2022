import os, re
from collections import defaultdict

# https://adventofcode.com/2022/day/23

DELTAS = [
    [(0,-1),(1,-1),(-1,-1)],  # N NE NW
    [(0,1),(1,1),(-1,1)],  # S SE SW
    [(-1,0),(-1,-1),(-1,1)], # W NW SW
    [(1,0),(1,-1),(1,1)], # E NE SE
]

def print_elves(elves):
    x_min = min([x for (x,_) in elves])
    y_min = min([y for (_,y) in elves])
    x_max = max([x for (x,_) in elves])
    y_max = max([y for (_,y) in elves])
    print()
    for y in range(y_min, y_max+1):
        ln = ''
        for x in range(x_min, x_max+1):
            if (x,y) in elves:
                ln += '#'
            else:
                ln += '.'
        print(ln)
    print()


#with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day23-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day23-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]
elves = set()
for y,line in enumerate(lines):
    for x,ch in enumerate(line):
        if ch == '#':
            elves.add((x,y))

dstart = 0
for _ in range(10):
    next = defaultdict(lambda: [])
    for (ex,ey) in elves:
        all_empty = True
        move_dir = (0,0)
        for di in range(dstart, dstart+4):
            deltas = DELTAS[di%4]
            found = True
            for dx,dy in deltas:
                if (ex+dx,ey+dy) in elves:
                    found = False
                    all_empty = False
                    break

            if found and move_dir == (0,0):
                # elf proposes to move one step in di direction
                move_dir = deltas[0]

        if all_empty:
            # stay where we are
            next[(ex,ey)] = [(ex,ey)]
        elif move_dir != (0,0):
            next[(ex+move_dir[0],ey+move_dir[1])].append((ex,ey))
        else:
            # stay put, nowehere to go
            next[(ex,ey)] = [(ex,ey)]

    elves = set()
    for (next_x,next_y),coming_from in next.items():
        if len(coming_from) > 1:
            # all stay put
            for nx,ny in coming_from:
                elves.add((nx,ny))
        else:
            elves.add((next_x, next_y))

    dstart = (dstart + 1) % 4

x_min = min([x for (x,_) in elves])
y_min = min([y for (_,y) in elves])
x_max = max([x for (x,_) in elves])
y_max = max([y for (_,y) in elves])
p1 = 0
for y in range(y_min, y_max+1):
    for x in range(x_min, x_max+1):
        if not (x,y) in elves:
            p1 += 1

#print_elves(elves)
print("Part 1: ", p1)
print("Part 2: ", )
