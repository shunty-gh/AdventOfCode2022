import os
from collections import Counter

# https://adventofcode.com/2022/day/9

def neighbours(p: tuple[int,int]) -> list[tuple[int,int]]:
    p0,p1 = p
    return [
        (p0, p1),
        (p0, p1-1),
        (p0+1, p1-1),
        (p0+1, p1),
        (p0+1, p1+1),
        (p0, p1+1),
        (p0-1, p1+1),
        (p0-1, p1),
        (p0-1, p1-1)]

def is_adjacent(hh, tt) -> bool:
    return tt in neighbours(hh)

def move_tail(hh: tuple[int, int], tt: tuple[int, int]) -> tuple[int, int]:
    if is_adjacent(hh, tt):
        return (0,0)

    if hh[0] == tt[0]:
        return (tt[0], tt[1]+1) if hh[1] > tt[1] else (tt[0], tt[1]-1)
    elif hh[1] == tt[1]:
        return (tt[0]+1, tt[1]) if hh[0] > tt[0] else (tt[0]-1, tt[1])
    else: # diagonal
        if hh[0] > tt[0] and hh[1] > tt[1]:
            return (tt[0]+1, tt[1]+1)
        elif hh[0] > tt[0] and hh[1] < tt[1]:
            return (tt[0]+1, tt[1]-1)
        elif hh[0] < tt[0] and hh[1] < tt[1]:
            return (tt[0]-1, tt[1]-1)
        else:
            return (tt[0]-1, tt[1]+1)

def do_moves(moves: list[tuple[str, int]], num_tails: int) -> int:
    dirs = { 'L': (-1, 0), 'R': (1,0), 'U': (0, -1), 'D': (0, 1)}
    v = Counter()
    head: tuple[int,int] = (0,0)
    tails: list[tuple[int,int]] = [(0,0)] * num_tails
    v[(0,0)] = 1
    for move in moves:
        dir = dirs[move[0]]
        count = move[1]
        for i in range(count):
            head = (head[0] + dir[0], head[1] + dir[1])
            for ti in range(len(tails)):
                t0 = head if ti == 0 else tails[ti-1]
                t1 = tails[ti]
                t_move = move_tail(t0, t1)
                if (t_move[0] != 0 or t_move[1] != 0):
                    tails[ti] = t_move
                    if ti == num_tails - 1:
                        v[t_move] += 1
    return len(v)

test_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
#lines = test_input.split('\n')
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day09-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]
lines = [line.split() for line in lines]
lines = [(x[0], int(x[1])) for x in lines]

print("Part 1: ", do_moves(lines, 1))
print("Part 2: ", do_moves(lines, 9))
