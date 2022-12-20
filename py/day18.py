import os

# https://adventofcode.com/2022/day/18 - Day 18: Boiling Boulders

def get_exposed(cubes: list[tuple[int,int,int]]) -> int:
    result = 0
    for (cx,cy,cz) in cubes:
        exposed = 6
        for (dx,dy,dz) in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
            if (cx+dx,cy+dy,cz+dz) in cubes:
                exposed -= 1
        result += exposed
    return result

# with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day18-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day18-input", "r") as f:
    lines = [line.strip().split(',') for line in f.readlines()]
cubes = [(int(l[0]),int(l[1]),int(l[2])) for l in lines]

all_exposed = get_exposed(cubes)

print("Part 1: ", all_exposed)