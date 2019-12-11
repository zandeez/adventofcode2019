#!/usr/bin/env python3
import asyncio
from typing import Dict, Tuple

from inputer import IntPuter, Pipe

Location = Tuple[int, int]


class Robot:
    def __init__(self, in_pipe: Pipe, out_pipe: Pipe):
        self.input_pipe: Pipe = in_pipe
        self.output_pipe: Pipe = out_pipe
        self.location: Location = (0, 0)
        self.direction: int = 0
        self.painted: Dict[Location, int] = {}

    def reset(self):
        self.location: Location = (0, 0)
        self.direction: int = 0
        self.painted: Dict[Location, int] = {}

    def step(self):
        if self.direction == 0:
            self.location = (self.location[0], self.location[1] - 1)
        elif self.direction == 1:
            self.location = (self.location[0] + 1, self.location[1])
        elif self.direction == 2:
            self.location = (self.location[0], self.location[1] + 1)
        else:
            self.location = (self.location[0] - 1, self.location[1])

    async def robot(self):
        while True:
            # Read current space into input queue
            current = self.painted.get(self.location, 0)
            # Send to IntPuter
            self.input_pipe.enqueue(current)
            # Read new colour and do paint
            paint = await self.output_pipe.dequeue()
            self.painted[self.location] = paint
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

# Reset systems
input_pipe.clear()
output_pipe.clear()
computer.reset()
robot.reset()
# Set initial point to a white square
robot.painted[(0, 0)] = 1
# Run tasks
loop.create_task(robot.robot())
loop.run_until_complete(computer.run_async())

# Calculate image size and offsets
xs, ys = [set(x) for x in zip(*robot.painted.keys())]
minx, maxx = min(xs), max(xs)
miny, maxy = min(ys), max(ys)
xo = 0 - minx
yo = 0 - miny
w, h = abs(maxx - minx) + 1, abs(maxy - miny) + 1

# Setup Picture
picture = [' '] * w * h

for k, v in sorted(robot.painted.items()):
    x, y = k
    if v == 1:
        picture[x + y * w] = '#'

print("Part 2:")

for x in range(0, w * h, w):
    print(''.join(picture[x:x + w]))
