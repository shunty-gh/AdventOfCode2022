import copy, math, os
from collections import Counter

# https://adventofcode.com/2022/day/11 - Day 11: Monkey in the Middle

def do_rounds(max_rounds: int, monkeys, is_part2: bool):
    div = 0
    if is_part2:
        div = math.prod([m['test'][0] for m in monkeys])

    inspections = Counter()
    for round in range(max_rounds):
        for i,monkey in enumerate(monkeys):
            for item in monkey['starts']:
                wl = item
                v = monkey['op'][2]
                v = wl if v == 'old' else int(v)
                if monkey['op'][1] == '+':
                    wl = wl + v
                else:
                    wl = wl * v
                if is_part2:
                    wl %= div
                else:
                    wl = wl // 3
                throw_to = monkey['test'][1]
                if wl % monkey['test'][0] != 0:
                    throw_to = monkey['test'][2]
                monkeys[throw_to]['starts'].append(wl)
                inspections[i] += 1
            monkey['starts'] = []

    vals = sorted(inspections.values())
    return vals[-1] * vals[-2]

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day11-input", "r") as f:
    monkey_notes = [line.split('\n') for line in f.read().split('\n\n')]

# eg
# Monkey 0:
#   Starting items: 56, 56, 92, 65, 71, 61, 79
#   Operation: new = old * 7
#   Test: divisible by 3
#     If true: throw to monkey 3
#     If false: throw to monkey 7

org_monkeys = []
for i,mn in enumerate(monkey_notes):
    mk = {
        'id': i,
        'starts': [int(m) for m in mn[1].strip()[len('Starting items: '):].split(', ')],
        'op': mn[2].strip().split('= ')[1].split(' '),
        'test': [int(mn[3].strip()[-2:]), int(mn[4].strip()[-2:]), int(mn[5].strip()[-2:])],
        }
    org_monkeys.append(mk)

print("Part 1: ", do_rounds(20, copy.deepcopy(org_monkeys), False))
print("Part 2: ", do_rounds(10000, copy.deepcopy(org_monkeys), True))
