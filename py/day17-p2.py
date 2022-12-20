import os

# https://adventofcode.com/2022/day/17 - Day 17: Pyroclastic Flow

# For part 2 max_rocks is 1000000000000
# This is way too big to run rock by rock so we need to find a shortcut. To this end we'll
# run a few thousand iterations and print out the differences in state.
# With some careful observation this should yield a repeating pattern at some point.
# ie after a certain number of iterations we should see the increases in tip height
# repeat. We will then use this information to calculate the final result.

# run this script and redirect the output to a file
# $> python3 day17-p2.py
#
# Open the file in a text editor with word wrap off
# Line one is rock index
# Line 2 is current tip
# Line 3 is the difference between the current tip and the previous tip
#
# Line 3 is where we want to find a repeating pattern
# Pick a start point. eg rock index 1000
# Select a few entries in line 3
# eg from 1000 to 1030
# Use the editor search to find a repeat of this sequence
# This will give the repeat period. Now find the point at which this
# repeat pattern starts by going back a few indexes until you find
# the point at which it doesn't repeat.

# For my data
# Repeat pattern found by selecting ~30 diff values and using the editor search function to find an identical set of diffs:
#    start at rock index 1000 with tip = 1580; pattern of diffs repeats at rock index 2720 with tip = 4282
# Repeat period = 2720-1000 = 1720
# Tip increase per repeat period = 4282-1580 = 2702
# Going back from 1000 we find that the repeating pattern starts at rock index 87 with a tip of 136
# Use the data as a look up table to find the increase in tip for the remaining number of steps
# In this case the remaining number of steps = (1000000000000-87) % 1720 = 1353
# Tip at index 87 = 136
# Tip at index 87+1353 = 2286
# Remainder = 2286-136 = 2150

SHOW_RESULT = True

if SHOW_RESULT:
    initindex = 87
    inittip = 136
    period = 1720
    tipinc = 2702
    remainder = 2150
    rocks = 1000000000000
    d1 = (rocks-initindex) // period
    #d2 = (rocks-initindex) % period
    part2 = inittip + (tipinc * d1) + remainder
    print("Part 2: ", part2)
    exit()

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
max_rocks = 5000
ri = 0
rbase = 0
last = 0
tower = dict()
tips, ris, diffs = [], [], []
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

    ris.append(ri)
    tips.append(tip)
    diffs.append(tip-last)
    last = tip

print(''.join(['{:6d}'.format(i) for i in ris]))
print(''.join(['{:6d}'.format(i) for i in tips]))
print(''.join(['{:6d}'.format(i) for i in diffs]))
