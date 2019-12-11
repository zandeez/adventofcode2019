#!/usr/bin/env python3
import asyncio

from inputer import IntPuter, Pipe

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

with open("day11.txt", "r") as f:
    code = f.readline()

input_pipe, output_pipe = Pipe(), Pipe()
computer = IntPuter(code, input_pipe, output_pipe)


class Robot:
    def __init__(self, input_pipe, output_pipe):
        self.x, self.y, self.direction = 0, 0, 0
        self.painted = {}
        self.input_pipe =input_pipe
        self.output_pipe = output_pipe

    def step(self):
        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y += 1
        else:
            self.x -= 1

    @asyncio.coroutine
    async def robot(self):
        while True:
            # Read current space into input queue
            current = self.painted.get((self.x, self.y), '0')
            # Send to IntPuter
            self.input_pipe.enqueue(current)
            # Read new colour and do paint
            paint = await self.output_pipe.dequeue()
            if paint != current:
                self.painted[(self.x, self.y)] = paint
            # Read move
            move = await self.output_pipe.dequeue()

            if move:
                self.direction = (self.direction + 1) % 4
            else:
                self.direction = (self.direction - 1) % 4

            self.step()

robot = Robot(input_pipe, output_pipe)
loop.create_task(robot.robot())
loop.run_until_complete(computer.run_async())

print("Part 1:", len(robot.painted))