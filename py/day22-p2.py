import os

# https://adventofcode.com/2022/day/22 - Day 22: Monkey Map

# Very specific solution based on the input. Need to build the next_pos method based
# on the format of the actual input.

DIR_DELTA = [(1,0), (0,1), (-1,0), (0,-1)]

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

# my cube input is of the form
#
#   ##
#   #
#  ##
#  #

FACES = [
    [( 50,  0),  ( 99, 49)],
    [(100,  0),  (149, 49)],
    [( 50, 50),  ( 99, 99)],
    [(  0,100),  ( 49,149)],
    [( 50,100),  ( 99,149)],
    [(  0,150),  ( 49,199)]
]

def next_pos(x, y, facing):
    (tl, br) = FACES[0]
    if x == tl[0] and y <= br[1] and facing == (-1,0): # -> left edge of face 1 joins left edge of face 4, upside down
        return (0, 149-y, (1,0))
    elif y == tl[1] and x >= tl[0] and x <= br[0] and facing == (0,-1): # top edge of f1 joins left edge of f6
        return (0, x+100, (1,0))

    (tl, br) = FACES[1]
    if y == tl[1] and x >= tl[0] and x <= br[0] and facing == (0,-1): # top edge of f2 joins bottom edge of f6
        return (x-100, 199, (0,-1))
    elif x == br[0] and y >= tl[1] and y <= br[1] and facing == (1,0):
        return (99, 149-y, (-1,0))
    elif y == br[1] and x >= tl[0] and x <= br[0] and facing == (0,1):
        return (99, x-50, (-1,0))

    (tl, br) = FACES[2]
    if x == tl[0] and y >= tl[1] and y <= br[1] and facing == (-1,0):
        return (y-50, 100, (0,1))
    elif x == br[0] and y >= tl[1] and y <= br[1] and facing == (1,0):
        return (y+50, 49, (0,-1))

    (tl, br) = FACES[3]
    if x == tl[0] and y >= tl[1] and y <= br[1] and facing == (-1,0):
        return (50, 149-y, (1,0))
    elif y == tl[1] and x >= tl[0] and x <= br[0] and facing == (0,-1):
        return (50, x+50, (1,0))

    (tl, br) = FACES[4]
    if x == br[0] and y >= tl[1] and y <= br[1] and facing == (1,0):
        return (149, 149-y, (-1,0))
    elif y == br[1] and x >= tl[0] and x <= br[0] and facing == (0,1):
        return (49, x+100, (-1,0))

    (tl, br) = FACES[5]
    if x == tl[0] and y >= tl[1] and y <= br[1] and facing == (-1,0):
        return (y-100, 0, (0,1))
    elif x == br[0] and y >= tl[1] and y <= br[1] and facing == (1,0):
        return (y-100, 149, (0,-1))
    elif y == br[1] and x >= tl[0] and x <= br[0] and facing == (0,1):
        return (x+100, 0, (0,1))

    # otherwise just move on one
    return (x+facing[0], y+facing[1], facing)

def turn(dirr, facing):
    fx, fy = facing
    return turn_l(fx, fy) if dirr == 'L' else turn_r(fx, fy)

def turn_l(fx, fy):
    return (fy, -fx)

def turn_r(fx, fy):
    return (-fy, fx)

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

x,y = map[0].index('.'),0
facing = (1,0)
ri = 0
while ri < len(route):
    dist = route[ri]
    # move - stop at walls, go round corners at edges
    for d in range(dist):
        nx, ny, nf = next_pos(x, y, facing)
        ch = map[ny][nx]

        if ch == '#': # wall, stop with current x,y
            break
        else: # update x,y and facing; move on
            x,y,facing = nx,ny,nf
    ri += 1

    # just checking
    if x < 0 or y < 0 or x > 149 or y > 199:
        raise KeyError("OOB")

    if ri < len(route):
        dirr = route[ri]
        facing = turn(dirr, facing)
        ri += 1

print("Part 2: ", (4 * (x+1)) + (1000 * (y+1)) + DIR_DELTA.index(facing))
