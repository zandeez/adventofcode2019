#!/usr/bin/env python3
from itertools import product

with open('day3.txt', 'r') as f:
    initial = f.readlines()

lines = []
for code in initial:
    line = []
    for instr in code.split(","):
        direction = instr[0]
        mag = int(instr[1:])
        if not line:
            prev = (0, 0, 0)
        else:
            prev = line[-1][1]
        if direction == "U":
            new = (prev[0], prev[1] + mag, prev[2] + mag)
        elif direction == "D":
            new = (prev[0], prev[1] - mag, prev[2] + mag)
        elif direction == "R":
            new = (prev[0] + mag, prev[1], prev[2] + mag)
        else:
            new = (prev[0] - mag, prev[1], prev[2] + mag)
        line.append((prev, new))
    lines.append(line)

intersections = []
for x, y in product(*lines):
    # Are lines the same orientation?
    if (x[0][0] == x[1][0] and y[0][0] == y[0][1]) or (x[0][1] == x[1][1] and y[0][1] == y[1][1]):
        continue
    xs, ys = sorted(x), sorted(y)
    if (xs[0][0] <= ys[0][0] <= xs[1][0]) \
            and (ys[0][1] <= xs[0][1] <= ys[1][1]):
        dist = x[0][2] + abs(x[0][0] - y[0][0]) + y[0][2] + abs(y[0][1] - x[0][1])
        intersections.append((ys[0][0], xs[0][1], dist))

print("Part 1:", sorted([abs(x) + abs(y) for x, y, z in intersections])[0])
print("Part 2:", sorted([z for x, y, z in intersections])[0])
