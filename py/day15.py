import os, re
from collections import defaultdict

# https://adventofcode.com/2022/day/15 - Day 15: Beacon Exclusion Zone

def get_distance(sensor: tuple[int,int], beacon: tuple[int,int]) -> int:
    (sx,sy), (bx,by) = sensor, beacon
    return abs(bx-sx) + abs(by-sy)

# eg Sensor at x=1290563, y=46916: closest beacon is at x=743030, y=-87472
ln_re = re.compile(r"Sensor at x=([-]?\d+), y=([-]?\d+): closest beacon is at x=([-]?\d+), y=([-]?\d+)")
### Test input. Expect P1: 26; P2: 56000011;
#y, maxcoord = 10, 20
#with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day15-test", "r") as f:
y, maxcoord = 2000000, 4000000
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day15-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]
sensors: dict[tuple[int,int], tuple[tuple[int,int], int]] = dict()
beacons = defaultdict(lambda: [])
for line in lines:
        match = ln_re.match(line)
        if (match):
            (sx, sy, bx, by) = [int(mg) for mg in match.groups()]
            sensors[(sx,sy)] = ((bx,by), get_distance((sx,sy), (bx,by)))
            beacons[(bx,by)].append((sx,sy))

covered: dict[tuple[int,int], int] = defaultdict(int)
for sensor,(_,d) in sensors.items():
    # does this sensor cover the y line
    sx = sensor[0]
    target = (sx,y)
    if get_distance(sensor, target) <= d:
        if not target in beacons:
            covered[target] += 1
    else:
        continue
    dx = 0
    oobL, oobR = False, False
    while oobL == False or oobR == False:
        dx += 1
        target = (sx+dx, y)
        if get_distance(sensor, target) <= d:
            if not target in beacons:
                covered[target] += 1
        else:
            oobR = True
        target = (sx-dx, y)
        if get_distance(sensor, target) <= d:
            if not target in beacons:
                covered[target] += 1
        else:
            oobL = True

print("Part 1: ", len([c for c in covered.values() if c > 0]))

# This takes a while - couple of minutes or so. We only skip forward in the x co-ord so
# the y advances slowly.
# There's bound to be a better way but I can't be bothered to look for it just yet.
part2 = (0,0)
in_range = True
for y in range(maxcoord + 1):
    x = 0
    while x <= maxcoord:
        pt = (x,y)
        in_range = False
        for (sx,sy),(_,d) in sensors.items():
            if get_distance((sx,sy), pt) <= d:
                in_range = True
                x = sx + (d - abs(y - sy)) # skip a chunk of x's that will still be in range of this sensor
                break
        if not in_range:
            part2 = (x,y)
            break
        x += 1
    if not in_range:
        break

#print(part2)
print("Part 2: ", part2[0] * 4_000_000 + part2[1])
