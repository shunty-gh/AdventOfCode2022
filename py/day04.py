import os

# https://adventofcode.com/2022/day/4

#test = "2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8".split('\n')
#input = [line.split(',') for line in test]
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day04-input", "r") as f:
    input = [line.strip().split(',') for line in f.readlines()]

part1 = 0
part2 = 0
input.reverse()
for i in input:
    l1,h1 = i[0].split('-')
    l2,h2 = i[1].split('-')
    l1,h1 = int(l1), int(h1)
    l2,h2 = int(l2), int(h2)
    if (l1 >= l2 and h1 <= h2) or (l2 >= l1 and h2 <= h1):
        part1 += 1

    if (l1 <= h2 and h1 >= l2) or (l2 <= h1 and h2 >= l1):
        part2 += 1

print("Part 1: ", part1)
print("Part 2: ", part2)
