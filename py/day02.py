import os

# https://adventofcode.com/2022/day/2 - Day 2: Rock Paper Scissors
# Why does modulo stuff mess with my brain so much

def points_for(x):
    return 1 if (x == "A" or x == "X") else 2 if (x == "B" or x == "Y") else 3

def get_score(a, b):
    pt_a = points_for(a)
    pt_b = points_for(b)
    win = pt_b % 3 == (pt_a + 1) % 3
    return pt_b + (3 if pt_a == pt_b else 6 if win else 0)

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day02-input", "r") as f:
    input = [line.strip() for line in f.readlines()]

part1 = 0 # sum(get_score(p1, p2) for (p1, p2) in [(play[0], play[1]) for play in [i.strip().split(' ') for i in input]])
part2 = 0

for (p1, p2) in [(play[0], play[1]) for play in [i.split(' ') for i in input]]:
    part1 += get_score(p1, p2)
    pp1 = points_for(p1)
    if p2 == "X": # Lose
        part2 += 3 if pp1 == 1 else (pp1 - 1) # or ((pp1 - 1 - 1 + 3) % 3) + 1 == ((pp1 + 1) % 3) + 1
    elif p2 == "Y": # Draw
        part2 += 3 + pp1
    else: # Win
        part2 += 6 + (1 if pp1 == 3 else (pp1 + 1)) # or ((pp1 - 1 + 1 + 3) % 3) + 1 == (pp1 % 3) + 1

print("Part 1:", part1)
print("Part 2:", part2)
