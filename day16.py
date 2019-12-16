#!/usr/bin/env python3
import itertools
from typing import List, Iterator


class FFT:
    PATTERN_TEMPLATE: List[int] = [0, 1, 0, -1]
    current_phase: List[int]

    def __init__(self, initial_phase: List[int]):
        self.current_phase = initial_phase

    def expand_pattern(self, number: int = 0) -> Iterator[int]:
        return itertools.islice(itertools.chain.from_iterable(
            [x] * number for x in itertools.cycle(FFT.PATTERN_TEMPLATE)
        ), 1, len(self.current_phase) + 1)

    def apply_phase(self):
        self.current_phase = [
            abs(sum(i * j for i, j in zip(self.current_phase, self.expand_pattern(stage + 1)))) % 10
            for stage in range(len(self.current_phase))
        ]

    def output(self, offset: int = 0):
        return ''.join([str(x) for x in fft.current_phase][offset:8])


with open("day16.txt", "r") as f:
    pattern = [
        int(x) for x in f.readline().strip()
    ]

fft = FFT(pattern)

for i in range(100):
    fft.apply_phase()

print("Part 1:", fft.output())

# offset = sum([
#     j * 10 ** i for i, j in enumerate(reversed(pattern[:7]))
# ])
#
# print(offset)
#
# fft = FFT(pattern*10000)
#
# for i in range(100):
#    fft.apply_phase()
#    print(i, fft.output())
#
# print("Part 2:", fft.output(offset))
