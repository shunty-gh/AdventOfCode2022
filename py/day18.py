import os
from collections import deque

# https://adventofcode.com/2022/day/18 - Day 18: Boiling Boulders

def get_exposed(cubes: set[tuple[int,int,int]]) -> int:
    result = 0
    for (cx,cy,cz) in cubes:
        exposed = 6
        for (dx,dy,dz) in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
            if (cx+dx,cy+dy,cz+dz) in cubes:
                exposed -= 1
        result += exposed
    return result

def is_outer_face(cube_face: tuple[int,int,int], cubes: set, outers: set, inners: set) -> bool:
    if cube_face in cubes or cube_face in inners:
        return False
    if cube_face in outers:
        return True

    # else - we're not sure yet
    # see if we can find any path to a known outer. Pick the smallest (x,y,z)
    target = (min([x for (x,_,_) in cubes]) - 1,
              min([y for (_,y,_) in cubes]) - 1,
              min([z for (_,_,z) in cubes]) - 1)
    visited = set()
    q = deque([cube_face])
    while len(q):
        cb = q.popleft()
        if cb in visited:
            continue
        visited.add(cb)

        if cb in outers:
            outers.update(visited)
            return True
        if cb in inners:
            inners.update(visited)
            return False

        # look at the neighbours
        (cx,cy,cz) = cb
        for (dx,dy,dz) in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
            nx = (cx+dx,cy+dy,cz+dz)
            if nx == target or nx in outers: # we're out in space, or at least we can definitely reach it
                outers.update(visited)
                return True
            if nx in inners: # we'll never make it out
                inners.update(visited)
                return False
            if nx in visited or nx in cubes: # no point looking here
                continue
            # otherwise add it to the queue
            q.append(nx)

    # can't find a way out
    inners.add(cube_face)
    return False

def get_exterior_area(cubes: set[tuple[int,int,int]]) -> int:
    result = 0
    outers = set()
    inners = set()
    for (cx,cy,cz) in cubes:
        for (dx,dy,dz) in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
            if is_outer_face((cx+dx,cy+dy,cz+dz), cubes, outers, inners):
                result += 1
    return result

#with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day18-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day18-input", "r") as f:
    lines = [line.strip().split(',') for line in f.readlines()]
cubes = set([(int(l[0]),int(l[1]),int(l[2])) for l in lines])

print("Part 1: ", get_exposed(cubes))
print("Part 2: ", get_exterior_area(cubes))
