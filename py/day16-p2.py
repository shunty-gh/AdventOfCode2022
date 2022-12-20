import os, re
from collections import defaultdict, deque

# https://adventofcode.com/2022/day/16 - Day 16: Proboscidea Volcanium (part 2)

###
# This is rubbish. It gives the correct result for the real data but is one out for the test data.
# It's also very slow.
# What I really ought to do is to pre-compute, at the start, the shortest distances between all
# the valves that have a flow > 0. Then use this information to help work out the routes. Also
# need a better visited/seen state check.
# Maybe sometime I'll get round to it but leave it for now.
#
# Big assumption - if we're at an unopened valve then we should open it if its flow rate is > 0
# I wonder if I could 'prove' this is ok somehow, but for now I'm just going to go for it.
###

def memo_key(t: int, rA: str, rB: str, states: str) -> str:
    return '{}__{}_{}_{}'.format(t, rA if rA < rB else rB, rB if rA < rB else rA, ':'.join(sorted(states.split(':'))))

def append_state(states: str, state: str) -> str:
    if states == '':
        return state
    return '{}:{}'.format(states, state)

def is_all_valves(states: str, all_valves_key: str) -> bool:
    return all_valves_key == ':'.join(sorted(states.split(':')))

# eg   "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
# and  "Valve JJ has flow rate=21; tunnel leads to valve II"
ln_re = re.compile(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
#with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day16-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day16-input", "r") as f:
    lines = [line.strip() for line in f.readlines()]

cave: dict[str, tuple[str, int, list[str]]] = {}
startindex = -1
for i,match in enumerate([ln_re.match(line) for line in lines]):
    if (match):
        mg = match.groups()
        caveid = mg[0]
        cave[caveid] = (caveid, int(mg[1]), mg[2].split(', '))


state_keys = {}
all_valves = ':'.join(sorted(cave.keys()))
max_time = 26
max_flow = 0
visited = {}
q: deque[tuple[str, str, int, str, int]] = deque([('AA', 'AA', 0, '', 0)])
while len(q) > 0:
    (roomIdA, roomIdB, flow, states, t) = q.popleft()

    if t >= max_time - 1: # no time left to do anything
        continue

    # have we already got a better flow for this state
    vk = memo_key(t, roomIdA, roomIdB, states)
    if vk in visited and visited[vk] > flow:
        continue

    (_, rateA, tunnelsA) = cave[roomIdA]
    (_, rateB, tunnelsB) = cave[roomIdB]

    # do we have rate > 0 for a valve that isn't yet turned on and enough time for it to make a difference
    if t < max_time - 1:
        # A opens valve, B opens valve
        mult = max_time - t - 1
        if rateA > 0 and not roomIdA in states and rateB > 0 and not roomIdB in states and roomIdA != roomIdB:
            newstates = append_state(append_state(states,roomIdA), roomIdB)
            newflow = flow + (rateA * mult) + (rateB * mult)
            if newflow > max_flow:
                max_flow = newflow
            if is_all_valves(newstates, all_valves):
                continue
            k = memo_key(t+1, roomIdA, roomIdB, newstates)
            if not k in visited or visited[k] < newflow:
                visited[k] = newflow
                q.append((roomIdA, roomIdB, newflow, newstates, t+1))

        # A opens valve, B moves
        elif rateA > 0 and not roomIdA in states:
            newstates = append_state(states, roomIdA)
            newflow = flow + (rateA * mult)
            if newflow > max_flow:
                max_flow = newflow
            if is_all_valves(newstates, all_valves):
                continue

            for ridB in tunnelsB:
                k1 = memo_key(t+1, roomIdA, ridB, newstates)
                if not k1 in visited or visited[k1] < newflow:
                    visited[k1] = newflow
                    q.append((roomIdA, ridB, newflow, newstates, t+1))

        # A moves, B opens valve
        elif rateB > 0 and not roomIdB in states:
            newstates = append_state(states, roomIdB)
            newflow = flow + (rateB * mult)
            if newflow > max_flow:
                max_flow = newflow
            if is_all_valves(newstates, all_valves):
                continue

            for ridA in tunnelsA:
                k1 = memo_key(t+1, ridA, roomIdB, newstates)
                if not k1 in visited or visited[k1] < newflow:
                    visited[k1] = newflow
                    q.append((ridA, roomIdB, newflow, newstates, t+1))

        else:
            # Both move to a different room without opening a valve
            #if t < max_time - 2: # no point in moving if there's no time left to do anything when you get there
                for ridA in tunnelsA:
                    for ridB in tunnelsB:
                        k1 = memo_key(t+1, ridA, ridB, states)
                        if not k1 in visited or visited[k1] < flow:
                            visited[k1] = flow
                            q.append((ridA, ridB, flow, states, t+1))

print("Part 2: ", max_flow)
