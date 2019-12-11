#!/usr/bin/env python3
from itertools import product, cycle
from math import atan2

planets = []

with open("day10.txt", "r") as f:
    lines = f.readlines()
    for i, y in enumerate(lines):
        for j, x in enumerate(y):
            if x == "#":
                planets.append({
                    'x': j,
                    'y': i,
                    'angles': {}
                })

for source, dest in product(planets, repeat=2):
    if source == dest:
        continue
    angle = atan2(dest['x'] - source['x'], dest['y'] - source['y'])
    if angle not in source['angles']:
        source['angles'][angle] = []
    source['angles'][angle].append(dest)

best_base = sorted(planets, key=lambda p: len(p['angles']), reverse=True)[0]
print("Part 1:", len(best_base['angles']))

for a in best_base['angles'].keys():
    best_base['angles'][a] = \
        sorted(best_base['angles'][a], key=lambda p: abs(p['y'] - best_base['y']) + abs(p['x'] - best_base['x']))

vaporised_count = 0
for angle in cycle(sorted(best_base['angles'].keys(), reverse=True)):
    if best_base['angles'][angle]:
        vaporised_count += 1
        planet = best_base['angles'][angle].pop(0)
        if vaporised_count == 200:
            print("Part 2:", planet['x']*100+planet['y'])
            break
