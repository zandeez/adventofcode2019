#!/usr/bin/env python3
from inputer import IntPuter, Pipe
from day15 import Droid


class Day17Droid(Droid):
    WALL = 46
    EMPTY = 35
    UNKNOWN = 10

    def find_intersections(self):
        return [k for k, v in self.grid if v == self.EMPTY and [l for l in self.next_locations(k) if self.grid.)


output_pipe = Pipe()
with open("day17.txt", "r") as f:
    computer = IntPuter(f.readline(), output_pipe=output_pipe)

computer.run()
droid = Day17Droid()
x, y = 0, 0
for i in output_pipe.data:
    if i == droid.UNKNOWN:
        y += 1
        x = 0
    else:
        droid.grid[(x, y)] = i

print(droid.grid)
