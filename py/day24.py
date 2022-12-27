import os
from collections import defaultdict

# https://adventofcode.com/2022/day/24 - Day 24: Blizzard Basin

def blow(wind,maxx,maxy):
    result = defaultdict(list)
    for (x,y),w in wind.items():
        for w1 in w:
            if w1 == '#':
                result[(x,y)] = ['#']
            elif w1 in ['<','>']:
                if w1 == '>':
                    nx = x+1 if x<maxx-1 else 1
                    result[(nx,y)].append(w1)
                else: # w1 == '<'
                    nx = x-1 if x>1 else maxx-1
                    result[(nx,y)].append(w1)
            else: # w1 in ['v','^']
                if w1 == 'v':
                    ny = y+1 if y<maxy-1 else 1
                    result[(x,ny)].append(w1)
                else: # w1 == '^'
                    ny = y-1 if y>1 else maxy-1
                    result[(x,ny)].append(w1)
    return result

def find_moves(x, y, wind, maxx, maxy):
    result = []
    for dx,dy in [(0,0),(1,0),(0,-1),(-1,0),(0,1)]:
        if x+dx >= 1 and x+dx <= maxx and y+dy>= 0 and y+dy <= maxy:
            c = (x+dx,y+dy)
            if not c in wind:
                result.append(c)
    return result

def draw(wind):
    xmax = max([x for (x,_) in wind])
    ymax = max([y for (_,y) in wind])
    for y in range(ymax+1):
        ln = ''
        for x in range(xmax+1):
            if (x,y) in wind:
                ln += wind[(x,y)][0] if len(wind[(x,y)]) == 1 else str(len(wind[(x,y)]))
            else:
                ln += '.'
        print(ln)
    print()

# with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day24-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day24-input", "r") as f:
    valley = [line.strip() for line in f.readlines()]

wind = defaultdict(list)
for y in range(len(valley)):
    for x in range(len(valley[0])):
        c = valley[y][x]
        if c in ['<','>','v','^','#']:
            wind[(x,y)] = [valley[y][x]]

entrance = (valley[0].index('.'),int(0))
exit = (valley[-1].index('.'),len(valley)-1)
max_x = len(valley[0])-1
max_y = len(valley)-1

q = set([entrance])
targets = [exit, entrance, exit]
target_index = 0
target = targets[target_index]
count, p1,p2 = 0,0,0
while p2 == 0:
    count += 1
    nextq = set()
    wind = blow(wind,max_x,max_y)
    # draw(wind)
    next_target = False
    for (cx,cy) in q:
        moves = find_moves(cx,cy, wind, max_x, max_y)
        for mx,my in moves:
            if (mx,my) == target:
                next_target = True
                if target_index == 0:
                    p1 = count
                elif target_index == 2:
                    p2 = count
                    break
                target_index += 1
                target = targets[target_index]
                nextq.clear()
            if not (mx,my) in nextq:
                nextq.add((mx,my))
        if next_target:
            break

    if len(nextq) == 0:
        break
    q = nextq

print("Part 1: ", p1)
print("Part 2: ", p2)
