import os

# https://adventofcode.com/2022/day/6 - Day 6: Tuning Trouble

def check_packet(pkt: str) -> tuple[bool, int]:
    for i in range(len(pkt)):
        if (pkt[i] in pkt[i+1:]):
            return (False, i+1)
    return (True, 0)

def scan_input(input: str, packet_len: int) -> int:
    i = 0
    while i < len(input):
        (success, index) = check_packet(input[i:i+packet_len])
        if success:
            return i + packet_len
        i += index
    raise IndexError("Unable to find an appropriate packet")

## main

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day06-input", "r") as f:
    data: str = f.read()

print("Part 1: ", scan_input(data, 4))
print("Part 2: ", scan_input(data, 14))
