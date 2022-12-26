import os

# https://adventofcode.com/2022/day/21 - Day 21: Monkey Math

def do_op(r1, op, r2) -> int:
    match op:
        case '+':
            return r1 + r2
        case '-':
            return r1 - r2
        case '*':
            return r1 * r2
        case '/':
            return r1 // r2
        case _:
            raise KeyError("Unknown operation {}".format(op))

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
    return do_op(r1, m[1], r2)

def load_data(data, mon, res):
    for d in data:
        mm = d[1].split()
        if len(mm) == 1:
            res[d[0]] = int(mm[0])
        else:
            mon[d[0]] = (mm[0], mm[1], mm[2])

def rewind_sum(id, target, mnkys):
    sm = mnkys[id]
    # one side is int, one side is id
    ll = sm[0]
    op = sm[1]
    rr = sm[2]
    next_target = 0
    # Do the opposite operation. Careful to get the operands the right way round.
    match op:
        case '+':
            if isinstance(rr, int):
                next_target = target - rr
            else:
                next_target = target - ll
        case '-':
            if isinstance(rr, int):
                next_target = target + rr
            else:
                next_target = ll - target
        case '*':
            if isinstance(rr, int):
                next_target = target // rr
            else:
                next_target = target // ll
        case '/':
            if isinstance(rr, int):
                next_target = target * rr
            else:
                next_target = ll // target
        case _:
            raise KeyError("Unknown operation {}".format(op))

    next_seek = ll if isinstance(rr, int) else rr
    if next_seek == 'humn':
        return next_target
    return rewind_sum(next_seek, next_target, mnkys)

#with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day21-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day21-input", "r") as f:
    data = [line.strip().split(': ') for line in f.readlines()]

## Part 1
monkeys1 ={}
resolved1 = {}
load_data(data, monkeys1, resolved1)
print("Part 1: ", resolve('root', monkeys1, resolved1))

## Part 2
monkeys2: dict[str, tuple[str|int,str,str|int]] = {}
resolved2: dict[str,int] = {}
load_data(data, monkeys2, resolved2)

# Resolve as many monkeys as we can, except 'humn', just by repeated lookups
changed = True
while changed:
    changed = False

    for mk,mv in monkeys2.items():
        if mk == 'humn':
            continue
        k1,k2 = mv[0], mv[2]
        if k1 != 'humn' and k1 in resolved2:
            rv = resolved2[k1]
            monkeys2[mk] = (rv, mv[1], mv[2])
            changed = True

        elif k2 != 'humn' and k2 in resolved2:
            rv = resolved2[k2]
            monkeys2[mk] = (mv[0], mv[1], rv)
            changed = True

        #  if we've worked out both sides of the sum then store it
        if isinstance(monkeys2[mk][0], int) and isinstance(monkeys2[mk][2], int):
            rr = do_op(monkeys2[mk][0], monkeys2[mk][1], monkeys2[mk][2])
            resolved2[mk] = rr

# At this point the monkeys should all have at least half of their sum resolved
# Now find the root and rewind the unresolved side of the sum until we get to 'humn'
root = monkeys2['root']
# one side is int, one side is id
seek = str(root[0] if isinstance(root[2], int) else root[2])
target = int(root[2] if isinstance(root[2], int) else root[0])
print("Part 2: ", rewind_sum(seek, target, monkeys2))
