#!/usr/bin/env python3
from inputer import IntPuter, Pipe

with open('day9.txt', 'r') as f:
    code = f.readline()

input_pipe, output_pipe = Pipe(), Pipe()
computer = IntPuter(code, input_pipe, output_pipe)
computer.reset()
input_pipe.enqueue(1)
computer.run()
print("Part 1:", output_pipe.data[0])

computer.reset()
input_pipe.enqueue(2)
computer.run()
print("Part 2:", output_pipe.data[1])
