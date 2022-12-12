from __future__ import annotations
import heapq, os, sys
from collections import defaultdict

# https://adventofcode.com/2022/day/12 - Day 12: Hill Climbing Algorithm

def get_neighbours(x, y, xmax, ymax):
    dd = [[1,0], [0,-1], [-1,0], [0,1]]
    return [[x+dx,y+dy] for dx,dy in dd if x+dx >= 0 and x+dx < xmax and y+dy >= 0 and y+dy < ymax]

def find_shortest(starts: list[tuple[int,int]], map: list[str]):
    maxX, maxY = len(map[0]), len(map)
    shortest_of_all = sys.maxsize
    for start in starts:
        to_visit = [(start,0)]
        costs = defaultdict(lambda: sys.maxsize)
        costs[start] = 0
        shortest = sys.maxsize
        while len(to_visit) > 0:
            (x,y),c = heapq.heappop(to_visit)
            if c >= shortest or c > costs[(x,y)]:
                continue

            curr = ord('a') if map[y][x] == 'S' else ord(map[y][x])
            neighbours = get_neighbours(x, y, maxX, maxY)
            for [nx,ny] in neighbours:
                nv = ord('z') if map[ny][nx] == 'E' else ord(map[ny][nx])
                can_visit = nv <= curr + 1
                if not can_visit:
                    continue
                cost = c + 1

                if cost < costs[(nx,ny)]:
                    costs[(nx,ny)] = cost
                    if map[ny][nx] == 'E':
                        shortest = cost
                    else:
                        heapq.heappush(to_visit, ((nx,ny), cost))

        if shortest < shortest_of_all:
            shortest_of_all = shortest

    return shortest_of_all

# test_input = """Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi"""
# lines = [line.strip() for line in test_input.splitlines()]
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day12-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]

# find the start
start = (0,0)
for y,line in enumerate(lines):
    if 'S' in line:
        x = line.index('S')
        start = (x,y)
        break

p1 = find_shortest([(start)], lines)

# find all potential starts ( == 'a' or == 'S)
possible_starts = []
for y,line in enumerate(lines):
    for x,ch in enumerate(line):
        if ch == 'a' or ch == 'S':
            possible_starts.append((x,y))

p2 = find_shortest(possible_starts, lines)

print("Part 1: ", p1)
print("Part 2: ", p2)
