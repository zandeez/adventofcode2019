#!/usr/bin/env python3
from itertools import permutations
from inputer import IntPuter, Pipe
import asyncio

with open('day7.txt', 'r') as f:
    code = f.readline()

computers = []
last_pipe = Pipe()
for i in range(5):
    next_pipe = Pipe()
    computers.append(
        IntPuter(code, last_pipe, next_pipe)
    )
    last_pipe = next_pipe

best_result = 0
best_settings = []

for p in permutations(range(0, 5)):
    for i, c in enumerate(computers):
        c.reset()
        c.input_pipe.clear()
        c.input_pipe.enqueue(p[i])

    computers[0].input_pipe.enqueue(0)
    computers[4].output_pipe.clear()

    for c in computers:
        c.run()

    result = computers[-1].output_pipe.peek()
    if result > best_result:
        best_result = result
        best_settings = p

print("Part 1:", best_result)

computers[0].input_pipe = computers[-1].output_pipe
best_result = 0
best_settings = []

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
for p in permutations(range(5, 10)):
    for i, c in enumerate(computers):
        c.reset()
        c.input_pipe.clear()
        c.input_pipe.enqueue(p[i])

    computers[0].input_pipe.enqueue(0)

    tasks = asyncio.gather(*[
        c.run_async() for c in computers
    ])
    loop.run_until_complete(tasks)

    result = computers[-1].output_pipe.peek()
    if result > best_result:
        best_result = result
        best_settings = p

print("Part 2:", best_result)
