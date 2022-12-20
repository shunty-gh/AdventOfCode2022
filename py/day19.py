import os, re
from collections import deque

# https://adventofcode.com/2022/day/19 - Day 19: Not Enough Minerals

# Very slow. About 9 minutes or so on my machine. But who cares anymore.
# Needs better methods of determining whether to add a state to the queue. But it works. Move on.

def query_append(qu: deque, st, key: tuple[int,int,int,int, int,int,int,int], tm: int):
    if not key in st or st[key] > tm:
        st[key] = tm
        qu.append((tm, key))

def run_blueprints(blueprints, max_minutes):
    results: dict[int, int] = {}
    for (bpId, orOre, clOre, obOre, obClay, geOre, geObs) in blueprints:
        # find the most 'expensive' builds
        max_ore_required = max(orOre, clOre, obOre, geOre)
        most_geodes = 0
        states = {}
        q = deque([(int(0),(int(1),int(0),int(0),int(0), int(0), int(0), int(0), int(0)))])
        while len(q) > 0:
            t, (orR, clR, obR, geR, ore, clay, obsidian, geodes) = q.popleft()

            k = (orR, clR, obR, geR, ore, clay, obsidian, geodes)
            if t > 0 and states[k] < t:
                continue
            if t > max_minutes:
                continue
            t += 1

            # crack some geodes
            new_geodes = geodes + geR
            if new_geodes > most_geodes:
                most_geodes = new_geodes

            if t == max_minutes:
                continue

            new_ore = ore + orR
            new_clay = clay + clR
            new_obs = obsidian + obR

            # can only build one robot
            # try and build a geode robot
            if obsidian >= geObs and ore >= geOre:
                query_append(q, states, (orR, clR, obR, geR+1, new_ore-geOre, new_clay, new_obs-geObs, new_geodes), t)
            # or an obsidian robot
            if clay >= obClay and ore >= obOre and obR < geObs:
                query_append(q, states, (orR, clR, obR+1, geR, new_ore-obOre, new_clay-obClay, new_obs, new_geodes), t)

            # ore or clay robot
            # if we've already got as many ore robots as needed than don't build any more
            if ore >= orOre and orR < max_ore_required:
                max_ore_usable = (max_minutes - t) * max_ore_required
                if ore < max_ore_usable:
                    query_append(q, states, (orR+1, clR, obR, geR, new_ore-orOre, new_clay, new_obs, new_geodes), t)
            # if we've already got as many clay robots as we can use then don't build any more
            # or if we've got more clay than we can possibly use
            if ore >= clOre and clR < obClay:
                max_clay_usable = (max_minutes - t) * obClay
                if clay < max_clay_usable:
                    query_append(q, states, (orR, clR+1, obR, geR, new_ore-clOre, new_clay, new_obs, new_geodes), t)

            # build nothing
            query_append(q, states, (orR, clR, obR, geR, new_ore, new_clay, new_obs, new_geodes), t)

        results[bpId] = most_geodes
    return results

# eg Blueprint 4: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 6 clay. Each geode robot costs 2 ore and 20 obsidian.
ln_re = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian")
#with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day19-test", "r") as f:
with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day19-input", "r") as f:
     lines = [line.strip() for line in f.readlines()]

blueprints: list[tuple[int,int,int,int,int,int,int]] = []
for line in lines:
        match = ln_re.match(line)
        if (match):
            bpId, oreRobotOre, clayRobotOre, obsRobotOre, obsRobotClay, geoRobotOre, geoRobotObs = [int(mg) for mg in match.groups()]
            blueprints.append((bpId, oreRobotOre, clayRobotOre, obsRobotOre, obsRobotClay, geoRobotOre, geoRobotObs))

p1 = run_blueprints(blueprints, 24)
print("Part 1: ", sum([bpid*ge for bpid,ge in p1.items()]))

p2 = run_blueprints(blueprints[:3], 32)
print("Part 2: ", p2[1] * p2[2] * p2[3])
