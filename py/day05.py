import copy, os, re

# https://adventofcode.com/2022/day/5

# line format "move 3 from 5 to 2"
mv_re = re.compile(r"move (\d{1,2}) from (\d{1,2}) to (\d{1,2})")
def move_crates(stacks: list[list[str]], moves: list[str], is_part2: bool) -> str:
    for move in moves:
        match = mv_re.match(move)
        if (match):
            from_count = (int)(match.group(1))
            from_stack_index = (int)(match.group(2))
            to_stack_index = (int)(match.group(3))

            from_stack = stacks[from_stack_index - 1]
            to_stack = stacks[to_stack_index - 1]

            if is_part2:
                tmp = []
                for i in range(from_count):
                    crate = from_stack.pop()
                    tmp.append(crate)

                for i in range(from_count):
                    crate = tmp.pop()
                    to_stack.append(crate)
            else:
                for i in range(from_count):
                    crate = from_stack.pop()
                    to_stack.append(crate)

    return stack_tops(stacks)

def stack_tops(stacks: list[list[str]]) -> str:
    result = ''
    for s in stacks:
        result += s[-1]
    return result

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day05-input", "r") as f:
    input = [line.strip() for line in f.readlines()]

# Can't be bothered to think up the necessary logic to read in the initial stack states
org_stacks: list[list[str]] = []
org_stacks.append(['G','D','V','Z','J','S','B'])
org_stacks.append(['Z','S','M','G','V','P'])
org_stacks.append(['C','L','B','S','W','T','Q','F'])
org_stacks.append(['H','J','G','W','M','R','V','Q'])
org_stacks.append(['C','L','S','N','F','M','D'])
org_stacks.append(['R','G','C','D'])
org_stacks.append(['H','G','T','R','J','D','S','Q'])
org_stacks.append(['P','F','V'])
org_stacks.append(['D','R','S','T','J'])

# "       [F] [Q]         [Q]
# [B]     [Q] [V] [D]     [S]
# [S] [P] [T] [R] [M]     [D]
# [J] [V] [W] [M] [F]     [J]     [J]
# [Z] [G] [S] [W] [N] [D] [R]     [T]
# [V] [M] [B] [G] [S] [C] [T] [V] [S]
# [D] [S] [L] [J] [L] [G] [G] [F] [R]
# [G] [Z] [C] [H] [C] [R] [H] [P] [D]
#  1   2   3   4   5   6   7   8   9 "

p1 = move_crates(copy.deepcopy(org_stacks), input[10:], False)
p2 = move_crates(copy.deepcopy(org_stacks), input[10:], True)

print("Part 1: ", p1)
print("Part 2: ", p2)
