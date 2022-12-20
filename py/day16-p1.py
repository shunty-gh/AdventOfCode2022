import os, re
from collections import deque

# https://adventofcode.com/2022/day/16 - Day 16: Proboscidea Volcanium (part 1)

# eg   "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
# and  "Valve JJ has flow rate=21; tunnel leads to valve II"
ln_re = re.compile(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
#with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day16-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day16-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]

cave: dict[str, tuple[str, int, list[str]]] = {}
for match in [ln_re.match(line) for line in lines]:
    if (match):
        mg = match.groups()
        cave[mg[0]] = (mg[0], int(mg[1]), mg[2].split(', '))

max_time = 30
max_flow = 0
all_valves_len = len(''.join([c[0] for c in cave.values() if c[1] > 0]))
visited = {}
q: deque[tuple[str, int, str, int]] = deque([('AA', 0, '', 0)])
while len(q) > 0:
    (roomId, flow, states, t) = q.popleft()

    if t >= max_time - 1: # no time left to do anything
        continue

    # have we already got a better rate for this state
    vk = (roomId, states, t)
    if vk in visited and visited[vk] > flow:
        continue

    (_, rate, tunnels) = cave[roomId]
    # do we have rate > 0 for a valve that isn't yet turned on and enough time for it to make a difference
    if rate > 0 and not roomId in states and t < max_time - 1:
        newstates = states + roomId
        newflow = flow + (rate * (max_time - t - 1))
        if newflow > max_flow:
            max_flow = newflow
        k = (roomId, newstates, t+1)
        if len(newstates) != all_valves_len and (not k in visited or visited[k] < newflow):
            visited[k] = newflow
            q.append((roomId, newflow, newstates, t+1))

    # And try and move to a different room without opening a valve
    if t < max_time - 2: # no point in moving if there's no time left to do anything when you get there
        for rid in tunnels:
            k1 = (rid, states, t+1)
            if not k1 in visited or visited[k1] < flow:
                visited[k1] = flow
                q.append((rid, flow, states, t+1))

print("Part 1: ", max_flow)
