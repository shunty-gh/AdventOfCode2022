import os

# https://adventofcode.com/2022/day/25

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

def to_SNAFU(src):
    result = []
    sl = len(src)
    s = src.copy()
    s.reverse()
    while len(s)>0:
        v = s[0]
        s = s[1:]
        if v <= 2:
            result.append(v)
        elif v == 3 or v == 4:
            if v == 3:
                result.append('=')
            else:
                result.append('-')
            i = 0
            while True:
                if len(s) > i:
                    s[i] += 1
                else:
                    s.append(1)
                if s[i] == 5:
                    s[i] = 0
                    i += 1
                else:
                    break
    result.reverse()
    return result

# with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day25-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day25-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]
sum = sum([fromSNAFU(s) for s in lines])
b5 = to_base5(sum)
p1 = to_SNAFU(b5)
print("Part 1: ", sum, b5,p1)
print("Part 1: ", ''.join([str(p) for p in p1]))
