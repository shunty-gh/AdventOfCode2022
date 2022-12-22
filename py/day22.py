import os

# https://adventofcode.com/2022/day/22 - Day 22: Monkey Map

def build_route(src: str) -> list:
    result = []
    s = src.strip()
    i, max_i = 0, len(s)
    while i < max_i:
        # Alternate num | dir
        ch = s[i]
        n = ''
        while ch >= '0' and ch <= '9':
            n += ch
            i += 1
            ch = src[i] if i < max_i else ''
        result.append(int(n))
        if ch != '':
            result.append(ch)
        i += 1
    return result

def turn(turn_letter, currently_facing):
    currently_facing += 1 if turn_letter == 'R' else -1
    return currently_facing % 4

#with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day22-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day22-input", "r") as f:
     mapstr, routestr = f.read().split('\n\n')
map = mapstr.splitlines()
route = build_route(routestr)

x_mod = max([len(l) for l in map])
y_mod = len(map)
# add trailing whitespace to make each line the same length
for i,ln in enumerate(map):
    if len(ln) < x_mod:
        map[i] += ' ' * (x_mod - len(ln))

x,y = 0,0
# find the initial start pos
ln = map[0]
while ln[x] == ' ':
    x += 1

dir_delta = [(1,0), (0,1), (-1,0), (0,-1)]
facing = 0
ri = 0
while ri < len(route):
    dist = route[ri]
    # move - skip empty spaces, stop at walls, wrap at edges
    dx,dy = dir_delta[facing]
    wall = False
    for d in range(dist):
        if wall:
            break
        nx,ny = x,y
        while True:
            nx,ny = (nx+dx) % x_mod, (ny+dy) % y_mod
            ch = map[ny][nx]
            if ch == '#': # wall, stop with current x,y
                wall = True
                break
            elif ch == '.': # update x,y; move on
                x,y = nx,ny
                break
            else: # empty space, skip over it
                pass
    ri += 1

    if ri < len(route):
        # turn
        dirr = route[ri]
        facing = turn(dirr, facing)
        ri += 1

print("Part 1: ", (4 * (x+1)) + (1000 * (y+1))+ facing)
print("Part 2: ", )
