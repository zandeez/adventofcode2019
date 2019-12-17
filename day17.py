#!/usr/bin/env python3
from typing import List, Tuple, Dict

from inputer import IntPuter, Pipe
from day15 import Droid

Location = Tuple[int, int]


class Day17Droid(Droid):
    WALL = ord('.')
    EMPTY = ord('#')
    UNKNOWN = ord('\n')

    DROID = [ord(x) for x in ['^', '>', 'v', '<']]

    direction: int = 0

    def find_intersections(self):
        return [k for k, v in self.grid.items() if v == self.EMPTY and len(
            [l for l in self.next_locations(k) if self.grid.get(l, self.UNKNOWN) == self.EMPTY]) == 4]

    def load_grid(self, data: List[int]):
        x, y = 0, 0
        for i in data:
            if i == self.UNKNOWN:
                y += 1
                x = 0
                print()
            else:
                if i in self.DROID:
                    self.location = (x, y)
                    self.direction = self.DROID.index(i)
                self.grid[(x, y)] = i
                x += 1
                print(chr(i), end='')

    def next_locations(self, location: Location = None) -> List[Location]:
        """
        Gets a list of adjacent locations to the current location. Ordered by direction as defined in the constants.

        Arguments:
        location -- location for which to find adjacent locations. Defaults to self.location if not set.
        """
        if location is None:
            location = self.location

        return [
            # North
            (location[0], location[1] - 1),
            # East
            (location[0] + 1, location[1]),
            # South
            (location[0], location[1] + 1),
            # West
            (location[0] - 1, location[1]),
        ]

    def walk_scaffold(self) -> str:
        instructions: str = ''
        count = 0
        while True:
            next_spaces = dict([(d, l)
                                for d, l in enumerate(self.next_locations()) if
                                self.grid.get(l, self.UNKNOWN) == self.EMPTY])
            if self.direction in next_spaces:
                count += 1
                self.location = next_spaces[self.direction]
            else:
                instructions += str(count)
                count = 0
                filtered_next = [(d, l) for d, l in next_spaces.items() if abs(
                    self.direction - d) % 2 == 1]
                if not filtered_next:
                    break
                next_dir, next_location = filtered_next.pop(0)
                if next_dir == 3 and self.direction == 0:
                    instructions += "L"
                elif next_dir == 0 and self.direction == 3:
                    instructions += "R"
                elif next_dir > self.direction:
                    instructions += "R"
                else:
                    instructions += "L"
                self.direction = next_dir

        return instructions.strip('0')

    def compress_commands(self):
        instructions = self.walk_scaffold()
        current_replacement = ord('A')
        commands: Dict[str, str] = {}
        while len(instructions.strip('ABC')):
            test_str = instructions.strip('ABC')
            for i in range(1, len(test_str)):
                if (test_str[-i:] not in test_str[:-i]) and i > 0 and 'A' not in test_str and 'B' not in test_str and 'C' not in test_str:
                    comp_str = test_str[:i-1]
                    commands[chr(current_replacement)] = comp_str
                    instructions = instructions.replace(comp_str, chr(current_replacement))
                    current_replacement += 1
                    break

        return instructions


output_pipe = Pipe()
with open("day17.txt", "r") as f:
    computer = IntPuter(f.readline(), output_pipe=output_pipe)

computer.run()
droid = Day17Droid()
droid.load_grid(computer.output_pipe.data)
intersections = droid.find_intersections()
print("Part 1:", sum([x * y for x, y in intersections]))
print(droid.compress_commands())
