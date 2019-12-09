#!/usr/bin/env python3
from inputer import IntPuter

with open('day5.txt', 'r') as f:
  computer = IntPuter(f.readline())

computer.reset()
computer.run()