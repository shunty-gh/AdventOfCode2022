import os

# https://adventofcode.com/2022/day/17

def fix_up(shape: list[tuple[int,int]], tip: int):
    # shift over by 2
    # shift up by tip + initial gap
    return [(x+2,y+tip+3+1) for (x,y) in shape]

# wind = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day17-input", "r") as f:
    wind = f.read()
    wind = wind.strip()

lh = [(0,0),(1,0),(2,0),(3,0)]
lv = [(0,0),(0,1),(0,2),(0,3)]
cross = [(1,0),(0,1),(1,1),(2,1),(1,2)]
ell = [(0,0),(1,0),(2,0),(2,1),(2,2)]
sq = [(0,0),(1,0),(0,1),(1,1)]
rocks = [lh, cross, ell, lv, sq]

wi = 0
wlen = len(wind)
rlen = len(rocks)
tip = 0
max_rocks = 2022
ri = 0
rbase = 0
last = 0
tower = dict()
while ri < max_rocks:
    # rock enters
    rock = fix_up(rocks[ri % rlen], tip)
    stopped = False
    while not stopped:
        # wind blows
        w = wind[wi % wlen]
        next = []
        if w == "<":
            next = [(x-1,y) for (x,y) in rock]
        else:
            next = [(x+1,y) for (x,y) in rock]
        blocked = False
        for p in next:
            if p[0] < 0 or p[0] >= 7 or p in tower:
                blocked = True
                break
        if not blocked:
            rock = next

        # rock drops
        next = [(x,y-1) for (x,y) in rock]
        for p in next:
            if p[1] <= 0 or p in tower:
                stopped = True
                break

        if stopped:
            for r in rock:
                tower[r] = 1
            tip = max(tip, max([y for (x,y) in rock]))
        else:
            rock = next

        wi += 1
    ri += 1

print("Part 1: ", tip)
