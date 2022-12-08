import os

# https://adventofcode.com/2022/day/8

test_input = """30373
25512
65332
33549
35390"""

def find_views(r, c, input):
    maxr = len(input) - 1
    maxc = len(input[0]) - 1
    org = int(input[r][c])
    r1 = r
    c1 = c
    v1, v2, v3, v4 = 0, 0, 0, 0
    while r1 > 0:
        r1 -= 1
        cv = int(input[r1][c])
        if cv < org:
            v1 += 1
        else:
            v1 += 1
            break
    r1 = r
    while r1 < maxr:
        r1 += 1
        cv = int(input[r1][c])
        if cv < org:
            v2 += 1
        else:
            v2 += 1
            break
    c1 = c
    while c1 > 0:
        c1 -= 1
        cv = int(input[r][c1])
        if cv < org:
            v3 += 1
        else:
            v3 += 1
            break
    c1 = c
    while c1 < maxc:
        c1 += 1
        cv = int(input[r][c1])
        if cv < org:
            v4 += 1
        else:
            v4 += 1
            break
    return v1 * v2 * v3 * v4

# lines = test_input.split('\n')
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day08-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]

rcount = len(lines)
ccount = len(lines[0])
visible = {}
for r in range(rcount):
    rhiL, rhiR = 0, 0
    for c in range(ccount):
        if r == 0 or c == 0 or r == rcount - 1 or c == ccount - 1:
            visible[(r,c)] = 1

        if int(lines[r][c]) > rhiL:
            visible[(r,c)] = 1
            rhiL = int(lines[r][c])
        if int(lines[r][ccount - 1 - c]) > rhiR:
            visible[(r,ccount-1-c)] = 1
            rhiR = int(lines[r][ccount - 1 - c])

for c in range(ccount):
    chiT, chiB = 0, 0
    for r in range(rcount):
        if int(lines[r][c]) > chiT:
            visible[(r,c)] = 1
            chiT = int(lines[r][c])
        if int(lines[rcount - 1 - r][c]) > chiB:
            visible[(rcount-1-r,c)] = 1
            chiB = int(lines[rcount - 1 - r][c])

views = {}
for r in range(rcount):
    for c in range(ccount):
        views[(r,c)] = find_views(r, c, lines)


print("Part 1: ", sum([v for v in visible.values() if v == 1]))
print("Part 2: ", max(v for v in views.values()))
#print(views)