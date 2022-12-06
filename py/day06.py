import copy, os, re

# https://adventofcode.com/2022/day/6 - Day 6: Tuning Trouble

def check_packet(pkt) -> bool:
    for i in range(len(pkt)):
        if (pkt[i] in pkt[i+1:]):
            return False
    return True

## main

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day06-input", "r") as f:
    input = f.read()

part1, part2 = 0, 0
for i in range(len(input)):
    if part1 == 0 and check_packet(input[i:i+4]):
        part1 = i + 4
    if part2 == 0 and  check_packet(input[i:i+14]):
        part2 = i + 14
    if part1 > 0 and part2 > 0:
        break

print("Part 1: ", part1)
print("Part 2: ", part2)
