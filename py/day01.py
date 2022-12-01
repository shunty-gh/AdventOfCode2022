import os

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day01-input", "r") as f:
    input = [line.strip() for line in f.readlines()]

part1 = 0
part2 = 0

s = 0
for i in input:
    if i == '':
        if s > part1:
            part1 = s
        s = 0
        continue

    s += int(i)

print("Part 1:", part1)
