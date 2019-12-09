#!/usr/bin/env python3
from inputer import IntPuter, Pipe

input_pipe, output_pipe = Pipe(), Pipe()

with open('day5.txt', 'r') as f:
    computer = IntPuter(f.readline(), input_pipe, output_pipe)

input_pipe.enqueue(1)
computer.run()
print("Part 1:", output_pipe.data[-1])

input_pipe.clear()
output_pipe.clear()
input_pipe.enqueue(5)
computer.reset()
computer.run()
print("Part 2:", output_pipe.data[-1])
