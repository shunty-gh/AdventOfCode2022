import os

# https://adventofcode.com/2022/day/3

def letter_score(ch):
    if ch >= 'a' and ch <= 'z':
        return 1 + ord(ch) - ord('a')
    else:
        return 27 + ord(ch) - ord('A')

#input = "vJrwpWtwJgWrhcsFMMfFFhFp\njqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\nPmmdzqPrVvPwwTWBwg\nwMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\nttgJtRGJQctTZtZT\nCrZsJsPPZsGzwwsLwLmpwMDw".split('\n')
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day03-input", "r") as f:
    input = [line.strip() for line in f.readlines()]

part1 = 0
for (ll, rr) in [(i[:len(i)//2],i[len(i)//2:]) for i in input]:
    for c in ll:
        if c in rr:
            part1 += letter_score(c)
            break

part2 = 0
for i in range(0, len(input), 3):
    for c in input[i]:
        if c in input[i+1] and c in input[i+2]:
            part2 += letter_score(c)
            break

print("Part 1: ", part1)
print("Part 2: ", part2)
