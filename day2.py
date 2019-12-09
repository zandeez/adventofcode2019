#!/usr/bin/env python3
import asyncio

from inputer import IntPuter


with open('day2.txt', 'r') as f:
  computer = IntPuter(f.readline())

## Part 1
computer.reset()
computer.set_loc(1, 12)
computer.set_loc(2, 2)
result = computer.run()
print("Part 1:", result[0])


computer.reset()

for i in range(0, len(computer.code)):
  for j in range(0, len(computer.code)):
    computer.reset()
    computer.set_loc(1, i)
    computer.set_loc(2, j)
    try:
      this_run = computer.run()
    except:
      pass
    else:
      if this_run[0] == 19690720:
        print ("Part 2:", i*100+j)
