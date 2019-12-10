#!/usr/bin/env python3
import itertools

with open('day3.txt', 'r') as f:
    initial = f.readlines()

lines = []
for code in initial:
    line = []
    for instr in code.split(","):
        dir = instr[0]
        mag = int(instr[1:])
        if not line:
            prev = (0, 0)
        else:
            prev = line[-1][1]
        if dir == "U":
            new = (prev[0], prev[1] + mag)
        elif dir == "D":
            new = (prev[0], prev[1] - mag)
        elif dir == "R":
            new = (prev[0] + mag, prev[1])
        else:
            new = (prev[0] - mag, prev[1])
        line.append((prev, new))
    lines.append(line)

for x, y in itertools.permutations(*lines):
    # check if both lines
    pass