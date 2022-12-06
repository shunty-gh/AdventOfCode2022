# https://adventofcode.com/2022/day/6 - Day 6: Tuning Trouble

# As day 6 is "Tuning Trouble" here is a solution with 2 approaches to scanning
# the packets along with tuning/timing information for the average time over 1000
# runs to show the improvement, if any, when skipping forward after finding a
# duplicate in the packet being checked.

def check_packet_and_skip(pkt: str) -> int:
    for i in range(len(pkt)):
        if (pkt[i] in pkt[i+1:]):
            return i
    return -1

def check_packet_bool(pkt: str) -> bool:
    for i in range(len(pkt)):
        if (pkt[i] in pkt[i+1:]):
            return False
    return True

def doit_with_skip(input: str) -> tuple[int, int]:
    """An improved version reducing the amount of scanning of previously seen sections"""

    part1, part2 = 0, 0
    i1, i2 = 0, 0
    for i in range(len(input)):
        if part1 == 0:
            cp = check_packet_and_skip(input[i1:i1+4])
            if cp < 0:
                part1 = i1 + 4
            i1 += cp + 1

        if part2 == 0:
            cp = check_packet_and_skip(input[i2:i2+14])
            if cp < 0:
                part2 = i2 + 14
            i2 += cp + 1

        if part1 > 0 and part2 > 0:
            break
    return (part1, part2)

def doit_full_scan(input: str) -> tuple[int, int]:
    """The original version - quick enough but with the potential for a lot of repeated scanning"""

    part1, part2 = 0, 0
    for i in range(len(input)):
        if part1 == 0 and check_packet_bool(input[i:i+4]):
            part1 = i + 4
        if part2 == 0 and  check_packet_bool(input[i:i+14]):
            part2 = i + 14

        if part1 > 0 and part2 > 0:
            break
    return (part1, part2)


if __name__ == '__main__':
    import os, timeit

    with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day06-input", "r") as f:
        data: str = f.read()

    t1 = timeit.Timer("doit_full_scan(data)", globals=globals());
    t2 = timeit.Timer("doit_with_skip(data)", globals=globals());
    t2time = t2.timeit(1000)
    t1time = t1.timeit(1000)
    print("Avg timings over *1000* repetitions:")
    print("  Full scan:", t1time / 1000)
    print("  With skip:", t2time / 1000)

    (p1, p2) = doit_full_scan(data);
    print("Part 1: ", p1)
    print("Part 2: ", p2)
