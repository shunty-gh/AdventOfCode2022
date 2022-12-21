import os

# https://adventofcode.com/2022/day/21

def resolve(id, data, resolved) -> int:
    if id in resolved:
        return resolved[id]

    if not id in data:
        raise KeyError("Monkey {} not found".format(id))
    m = data[id]
    r1 = resolve(m[0], data, resolved)
    r2 = resolve(m[2], data, resolved)
    resolved[m[0]] = r1
    resolved[m[2]] = r2

    match m[1]:
        case '+':
            return r1 + r2
        case '-':
            return r1 - r2
        case '*':
            return r1 * r2
        case '/':
            return r1 // r2
        case _:
            raise KeyError("Unknown operation {}".format(m[1]))

def load_data(data, mon, res):
    for d in data:
        mm = d[1].split()
        if len(mm) == 1:
            res[d[0]] = int(mm[0])
        else:
            mon[d[0]] = (mm[0], mm[1], mm[2])

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day21-input", "r") as f:
    data = [line.strip().split(': ') for line in f.readlines()]
resolved = {}
monkeys ={}
load_data(data, monkeys, resolved)
print("Part 1: ", resolve('root', monkeys, resolved))
