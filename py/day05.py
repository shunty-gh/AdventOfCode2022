import copy, os, re

# https://adventofcode.com/2022/day/5 - Day 5: Supply Stacks

# line format: "move 3 from 5 to 2"
mv_re = re.compile(r"move (\d{1,2}) from (\d{1,2}) to (\d{1,2})")
def move_crates(stacks: list[list[str]], moves: list[str], is_part2: bool) -> str:
    for move in moves:
        match = mv_re.match(move)
        if (match):
            (from_count, from_index, to_index) = [int(mg) for mg in match.groups()]
            from_stack = stacks[from_index - 1]
            to_stack = stacks[to_index - 1]

            if is_part2:
                to_stack.extend(from_stack[-from_count:])
                del from_stack[-from_count:]
            else:
                for i in range(from_count):
                    to_stack.append(from_stack.pop())

    return str.join('', [s[-1] for s in stacks])

## main

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day05-input", "r") as f:
    input = [line.strip('\n') for line in f.readlines()] # need the leading spaces for the stack defn

# Assume 9 stack definition rows and moves start on 11th row
stack_def = reversed(input[:8]) # skip the stack indexes row
org_stacks: list[list[str]] = [[],[],[],[],[],[],[],[],[]]
for sd in stack_def:
    for i, ci in enumerate(range(1, 34, 4)): # crate letters are evey 4th char starting at ch pos 1
        if len(sd) <= ci:
            break
        if sd[ci] != ' ':
            org_stacks[i].append(sd[ci])

print("Part 1: ", move_crates(copy.deepcopy(org_stacks), input[10:], False))
print("Part 2: ", move_crates(copy.deepcopy(org_stacks), input[10:], True))
