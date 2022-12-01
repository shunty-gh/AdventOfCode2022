import os

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day01-input", "r") as f:
    input = [line.strip() for line in f.readlines()]

sums = []
s = 0
for i in input:
    if i == '':
        sums.append(s)
        s = 0
        continue

    s += int(i)
# Don't forget the last one!
if s > 0:
    sums.append(s)

sums.sort(reverse=True)
print("Part 1:", sums[0])
print("Part 2:", sums[0] + sums[1] + sums[2])
