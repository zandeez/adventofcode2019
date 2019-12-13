#!/usr/bin/env python3
from typing import List

from inputer import IntPuter, Pipe
import asyncio


class Display(Pipe):

    def __init__(self, input_pipe: Pipe):
        super().__init__()
        self.input_pipe: Pipe = input_pipe
        self.state: List[List[int]] = []
        self.score: int = 0
        self.location: int = 0
        self.ball: int = 0

    def remaining_blocks(self) -> int:
        return sum([len([x for x in row if x == 2]) for row in self.state])

    async def dequeue(self) -> int:
        return int((self.location < self.ball) - (self.location > self.ball))

    async def run(self):
        first_run = True
        while self.remaining_blocks() or first_run:
            x = await self.input_pipe.dequeue()
            y = await self.input_pipe.dequeue()
            o = await self.input_pipe.dequeue()

            if first_run and o == 2:
                first_run = False

            if x < 0:
                self.score = o
                continue

            if y >= len(self.state):
                for d in range(y - len(self.state) + 1):
                    self.state.append([])

            if x >= len(self.state[y]):
                for d in range(x - len(self.state[y]) + 1):
                    self.state[y].append(0)

            self.state[y][x] = o

            if o == 3:
                self.location = x
            elif o == 4:
                self.ball = x

        x = await self.input_pipe.dequeue()
        y = await self.input_pipe.dequeue()
        o = await self.input_pipe.dequeue()
        self.score = o


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

output_pipe = Pipe()
display = Display(output_pipe)
with open("day13.txt", "r") as f:
    computer = IntPuter(f.readline(), display, output_pipe)

task = loop.create_task(display.run())
loop.run_until_complete(computer.run_async())
task.cancel()

print("Part 1:", display.remaining_blocks())

computer.reset()
output_pipe.clear()
computer.set_loc(0, 2)
loop.run_until_complete(asyncio.gather(computer.run_async(), display.run()))

print("Part 2:", display.score)
