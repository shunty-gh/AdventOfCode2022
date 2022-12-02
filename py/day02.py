import os

def points_for(x):
    return 1 if x == "A" else 2 if x == "B" else 3

def get_score(a,b):
    p = points_for(b)
    if a == b:
        return 3 + p
    elif a == "A":
        if b == "B":
            return 6 + p
        else:
            return p
    elif a == "B":
        if b == "A":
            return p
        else:
            return 6 + p
    else:
        if b == "A":
            return 6 + p
        else:
            return p

with open(os.path.dirname(os.path.realpath(__file__)) + "/../input/day02-input", "r") as f:
    input = [line.strip() for line in f.readlines()]

score1 = 0
score2 = 0
map = { "X": "A", "Y": "B", "Z": "C" }
for i in input:
    sp = i.split(' ')
    score1 += get_score(sp[0], map[sp[1]])
    if sp[1] == "X": # Lose
        play = "C" if sp[0] == "A" else "A" if sp[0] == "B" else "B"
        score2 += get_score(sp[0], play)
    elif sp[1] == "Y": # Draw
        score2 += get_score(sp[0], sp[0])
    else: # Win
        play = "B" if sp[0] == "A" else "C" if sp[0] == "B" else "A"
        score2 += get_score(sp[0], play)

print("Part 1:", score1)
print("Part 2:", score2)
