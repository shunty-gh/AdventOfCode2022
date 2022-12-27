import os

# https://adventofcode.com/2022/day/25 - Day 25: Full of Hot Air

def fromSNAFU(snum):
    result = 0
    sl = len(snum)
    n = 0
    for i in range(sl):
        match snum[sl-i-1]:
            case '-':
                n = -1
            case '=':
                n = -2
            case '2':
                n = 2
            case '1':
                n = 1
            case '0':
                n = 0
        result += pow(5,i) * n

    return result

def to_base5(n):
    result = []
    x = n
    while x > 0:
        result.append(x % 5)
        x = x // 5
    result.reverse()
    return result

def to_SNAFU(num):
    src = to_base5(num)
    result = []
    src.reverse()
    while len(src)>0:
        v = src[0]
        src = src[1:]
        if v <= 2:
            result.append(v)
        elif v == 3 or v == 4:
            if v == 3:
                result.append('=')
            else:
                result.append('-')
            i = 0
            while True:
                if len(src) > i:
                    src[i] += 1
                else:
                    src.append(1)
                if src[i] == 5:
                    src[i] = 0
                    i += 1
                else:
                    break
    result.reverse()
    return ''.join([str(n) for n in result])

# with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day25-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day25-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]
p1 = sum([fromSNAFU(s) for s in lines])
p2 = to_SNAFU(p1)
print("Part 1: ", p1)
print("Part 2: ", p2)
