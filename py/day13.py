import os

# https://adventofcode.com/2022/day/13 - Day 13: Distress Signal

def parse_list(lststr: str):
    """ Parse a string of the form [[1],[2,3,4]] into an appropriate list of lists and ints """

    assert(lststr[0] == '[' and lststr [-1] == ']')
    src = lststr[1:len(lststr)-1] # ignore the leading and trailing '[',']' characters
    result = []
    last = result
    curr = result
    nextintstr = ''
    for c in src:
        match c:
            case '[':
                # start new sub-list
                last = curr
                curr.append([])
                curr = curr[-1]
            case ']':
                # end current list, go back to prior list
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

def compare_elements(el: list | int, er: list | int) -> int:
    """ Determine if el 'is less than' er. Return 1 if so or 0 if 'equal' or -1 if er < el """

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
    else: # only one or the other is a list
        if isinstance(el, list):
            return compare_elements(el, [er])
        else:
            return compare_elements([el], er)

# pairs = ("[1,1,3,1,1]\n[1,1,5,1,1]\n\n"
# "[[1],[2,3,4]]\n[[1],4]\n\n"
# "[9]\n[[8,7,6]]\n\n"
# "[[4,4],4,4]\n[[4,4],4,4,4]\n\n"
# "[7,7,7,7]\n[7,7,7]\n\n"
# "[]\n[3]\n\n"
# "[[[]]]\n[[]]\n\n"
# "[1,[2,[3,[4,[5,6,7]]]],8,9]\n[1,[2,[3,[4,[5,6,0]]]],8,9]"
# ).split('\n\n')
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day13-input", "r") as f:
    pairs = f.read().strip().split('\n\n')
pairs = [pair.split('\n') for pair in pairs]
packets = [(parse_list(p1), parse_list(p2)) for (p1, p2) in pairs]

# Part 1
valid_pairs = []
for i, (p1, p2) in enumerate(packets):
    if compare_elements(p1, p2) >= 0:
        valid_pairs.append(i+1)

print("Part 1: ", sum(valid_pairs))

# Part 2
# No need to sort. Just find how many items are less than d1 and d2
d1, d2 = parse_list('[[2]]'), parse_list('[[6]]')
id1, id2 = 0, 0
for p1, p2 in packets:
    id1 += 1 if compare_elements(p1, d1) > 0 else 0
    id1 += 1 if compare_elements(p2, d1) > 0 else 0
    id2 += 1 if compare_elements(p1, d2) > 0 else 0
    id2 += 1 if compare_elements(p2, d2) > 0 else 0

# don't forget they're zero indexed and d2 is also greater than d1
print("Part 2: ", (id1+1)*(id2+2))
