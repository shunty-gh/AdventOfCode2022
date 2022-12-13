import os, sys
from collections import defaultdict, deque
from functools import cmp_to_key

# https://adventofcode.com/2022/day/13

def parse_list(lststr: str):
    result: list[list[int] | int] = []
    last = result
    curr: list[list[int] | int] = result
    nextintstr = ''
    src = lststr[1:len(lststr)-1]
    for c in src:
        match c:
            case '[':
                # start new list
                ls = []
                last = curr
                curr.append(ls)
                curr = ls
            case ']':
                # end current list, if any, append it, start new one
                if nextintstr != '':
                    curr.append(int(nextintstr))
                    nextintstr = ''
                curr = last
            case ',':
                if nextintstr != '':
                    curr.append(int(nextintstr))
                    nextintstr = ''
            case _: # int
                nextintstr += c
    if nextintstr != '':
        curr.append(int(nextintstr))

    return result

def compare_elements(el, er) -> int:
    if isinstance(el, int) and isinstance(er, int):
        return 1 if el < er else 0 if el == er else -1
    elif isinstance(el, list) and isinstance(er, list):
        for i, li in enumerate(el):
            if len(er) < i + 1:
                return -1
            res = compare_elements(li, er[i])
            if res != 0:
                return res
        return 0 if len(el) == len(er) else 1
    else:
        if isinstance(el, list):
            return compare_elements(el, [er])
        else:
            return compare_elements([el], er)

def compare_pair(ll, rr) -> int:
    left = parse_list(ll)
    right = parse_list(rr)
    return compare_elements(left, right)


# pairs = """[1,1,3,1,1]
# [1,1,5,1,1]

# [[1],[2,3,4]]
# [[1],4]

# [9]
# [[8,7,6]]

# [[4,4],4,4]
# [[4,4],4,4,4]

# [7,7,7,7]
# [7,7,7]

# []
# [3]

# [[[]]]
# [[]]

# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]""".split('\n\n')
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day13-input", "r") as f:
    pairs = f.read().strip().split('\n\n')
pairs = [pair.split('\n') for pair in pairs]

# Part 1
valid_pairs = []
for i, (p1, p2) in enumerate(pairs):
    if compare_pair(p1, p2) >= 0:
        valid_pairs.append(i+1)

print("Part 1: ", sum(valid_pairs))

# Part 2
packets = []
for p1, p2 in pairs:
    packets.append(parse_list(p1))
    packets.append(parse_list(p2))

# no need to sort. Just find how many items are less than d1 and d2
d1 = parse_list('[[2]]')
d2 = parse_list('[[6]]')
id1, id2 = 0, 0
for p in packets:
    if compare_elements(p, d1) > 0:
        id1 += 1
    if compare_elements(p, d2) > 0:
        id2 += 1

# don't forget zero indexed and d2 is also greater than d1
print("Part 2: ", (id1+1)*(id2+2))
