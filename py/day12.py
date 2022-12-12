import os, sys
from collections import defaultdict, deque

# https://adventofcode.com/2022/day/12 - Day 12: Hill Climbing Algorithm

def get_neighbours(x, y, xmax, ymax):
    dd = [[1,0], [0,-1], [-1,0], [0,1]]
    return [[x+dx,y+dy] for dx,dy in dd if x+dx >= 0 and x+dx < xmax and y+dy >= 0 and y+dy < ymax]

def find_shortest(starts: list[tuple[int,int]], map: list[str]):
    maxX, maxY = len(map[0]), len(map)
    shortest_of_all = sys.maxsize
    for start in starts:
        to_visit: deque[tuple[tuple[int,int],int]] = deque([(start,0)])
        costs = defaultdict(lambda: sys.maxsize)
        costs[start] = 0
        shortest = sys.maxsize
        while len(to_visit) > 0:
            (x,y),c = to_visit.popleft()
            if c >= shortest or c > costs[(x,y)]:
                continue

            curr = ord('a') if map[y][x] == 'S' else ord(map[y][x])
            for [nx,ny] in get_neighbours(x, y, maxX, maxY):
                nv = ord('z') if map[ny][nx] == 'E' else ord(map[ny][nx])
                if nv > curr + 1:
                    continue

                cost = c + 1
                if cost < costs[(nx,ny)]:
                    costs[(nx,ny)] = cost
                    if map[ny][nx] == 'E':
                        shortest = cost
                    else:
                        to_visit.append(((nx,ny), cost))

        if shortest < shortest_of_all:
            shortest_of_all = shortest

    return shortest_of_all

#lines = """Sabqponm\nabcryxxl\naccszExk\nacctuvwj\nabdefghi""".splitlines()
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day12-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]

# P1: find the start position ( == 'S')
sy = next(y for y,line in enumerate(lines) if 'S' in line)
start = (lines[sy].index('S'),sy)
p1 = find_shortest([start], lines)

# P2: find all potential starts ( == 'a' or == 'S)
possible_starts = [start]
for y,line in enumerate(lines):
    possible_starts.extend([(x,y) for x,ch in enumerate(line) if ch == 'a'])
p2 = find_shortest(possible_starts, lines)

print("Part 1: ", p1)
print("Part 2: ", p2)
