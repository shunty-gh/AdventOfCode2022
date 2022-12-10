import os

# https://adventofcode.com/2022/day/10

def write_to_crt_buffer(cy: int, x: int, scr: list[str]):
    if (cy-1) % 40 in [x-1,x,x+1]:
        scr.append('#')
    else:
        scr.append(' ')

def check_freq(cy: int, x: int, fr: dict[int, int]):
    if cy % 20 == 0:
        fr[cy] = cy * x

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day10-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]

regX = 1
cycle = 1
freqs = {}
crt = ['#']
for line in lines:
    match line:
        case 'noop':
            cycle += 1
            check_freq(cycle, regX, freqs)
            write_to_crt_buffer(cycle, regX, crt)
        case _:  # addx
            spl = line.split()
            cycle += 1
            check_freq(cycle, regX, freqs)
            write_to_crt_buffer(cycle, regX, crt)
            cycle += 1
            regX += int(spl[1])
            check_freq(cycle, regX, freqs)
            write_to_crt_buffer(cycle, regX, crt)

p1 = sum(v for k,v in freqs.items() if k in [20,60,100,140,180,220])
print("Part 1: ", p1)
print("Part 2: ")
for i in range(6):
    ln = ''.join(crt[i*40:(i*40)+40])
    print(ln)