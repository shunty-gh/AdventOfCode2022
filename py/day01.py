import os

# https://adventofcode.com/2022/day/1 - Day 1: Calorie Counting

#input = [line.strip() for line in '1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000'.split('\n')]
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day01-input", "r") as f:
    input = [line.strip() for line in f.readlines()]

sums = [0]
for i in input:
    if i == '':
        sums.append(0)
        continue

    sums[-1] += int(i)

sums.sort(reverse=True)
print("Part 1:", sums[0])
print("Part 2:", sum(sums[0:3]))
