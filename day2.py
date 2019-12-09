#!/usr/bin/env python3
from inputer import IntPuter
from itertools import product

with open('day2.txt', 'r') as f:
    computer = IntPuter(f.readline())

## Part 1
computer.set_loc(1, 12)
computer.set_loc(2, 2)
result = computer.run()
print("Part 1:", result[0])

## Part 2
for i, j in product(range(0, len(computer.code)), repeat=2):
    computer.reset()
    computer.set_loc(1, i)
    computer.set_loc(2, j)
    try:
        this_run = computer.run()
    except:
        pass
    else:
        if this_run[0] == 19690720:
            print("Part 2:", i * 100 + j)
            break