import os
from collections import Counter

# https://adventofcode.com/2022/day/9 - Day 9: Rope Bridge

def neighbours(p: tuple[int,int]) -> list[tuple[int,int]]:
    p0,p1 = p
    return [
        (p0, p1), (p0, p1-1), (p0+1, p1-1),
        (p0+1, p1), (p0+1, p1+1), (p0, p1+1),
        (p0-1, p1+1), (p0-1, p1), (p0-1, p1-1)
        ]

def move_tail(hh: tuple[int, int], tt: tuple[int, int]) -> tuple[int, int]:
    if (tt in neighbours(hh)):
        return (0,0)

    if hh[0] == tt[0]:
        return (0, 1) if hh[1] > tt[1] else (0, -1)
    elif hh[1] == tt[1]:
        return (1, 0) if hh[0] > tt[0] else (-1, 0)
    else: # diagonal
        tt0 = 1 if hh[0] > tt[0] else -1
        tt1 = 1 if hh[1] > tt[1] else -1
        return (tt0, tt1)

def do_moves(moves: list[tuple[str, int]], num_tails: int) -> int:
    dir_deltas = { 'L': (-1, 0), 'R': (1,0), 'U': (0, -1), 'D': (0, 1)}
    visited = Counter()
    rope: list[tuple[int,int]] = [(0,0)] * (num_tails+1)
    visited[(0,0)] = 1
    for dir, dist in moves:
        dx,dy = dir_deltas[dir]
        for _ in range(dist):
            rope[0] = (rope[0][0] + dx, rope[0][1] + dy)
            for ti in range(1, len(rope)):
                t0 = rope[ti-1]
                t1 = rope[ti]
                t_move = move_tail(t0, t1)
                rope[ti] = (t1[0]+t_move[0], t1[1]+t_move[1])
                if ti == num_tails:  # strictly speaking '...and t_move != (0,0)'
                    visited[rope[ti]] += 1
    return len(visited)

#test_input = "R 4\nU 4\n\nL 3\nD 1\nR 4\nD 1\nL 5\nR 2"
#lines = test_input.split('\n')
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day09-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]
lines = [line.split() for line in lines]
lines = [(x[0], int(x[1])) for x in lines]

print("Part 1: ", do_moves(lines, 1))
print("Part 2: ", do_moves(lines, 9))
