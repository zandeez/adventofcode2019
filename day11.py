#!/usr/bin/env python3
import asyncio
from itertools import product
from typing import Dict, Tuple

from inputer import IntPuter, Pipe


class Robot:
    def __init__(self, input_pipe, output_pipe):
        self.input_pipe = input_pipe
        self.output_pipe = output_pipe
        self.reset()

    def reset(self):
        self.x, self.y, self.direction = 0, 0, 0
        self.painted: Dict[Tuple[int, int], int] = {}

    def step(self):
        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y += 1
        else:
            self.x -= 1

    async def robot(self):
        while True:
            # Read current space into input queue
            location = (self.x, self.y)
            current = self.painted.get(location, 0)
            # Send to IntPuter
            self.input_pipe.enqueue(current)
            # Read new colour and do paint
            paint = await self.output_pipe.dequeue()
            self.painted[location] = paint
            # Read move
            move = await self.output_pipe.dequeue()

            if move:
                self.direction = (self.direction + 1) % 4
            else:
                self.direction = (self.direction - 1) % 4

            self.step()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

with open("day11.txt", "r") as f:
    code = f.readline()

input_pipe, output_pipe = Pipe(), Pipe()
computer = IntPuter(code, input_pipe, output_pipe)

robot = Robot(input_pipe, output_pipe)
loop.create_task(robot.robot())
loop.run_until_complete(computer.run_async())

print("Part 1:", len(robot.painted))

input_pipe.clear()
output_pipe.clear()
computer.reset()
robot.reset()
robot.painted[(0, 0)] = 1
loop.create_task(robot.robot())
loop.run_until_complete(computer.run_async())

xs, ys = [set(x) for x in zip(*robot.painted.keys())]
minx, maxx = min(xs), max(xs)
miny, maxy = min(ys), max(ys)
xo = 0 - minx
yo = 0 - miny

picture = [
              [' '] * (maxx - minx + 1)
          ] * (maxy - miny + 1)

for x, y in product(xs, ys):
    if robot.painted.get((x, y), 0):
        picture[y][x] = '#'

print("Part 2:")

for row in picture:
    print(''.join(row))
