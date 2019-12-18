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
            candidates: List[Tuple[int, str]] = []
            test_str = instructions.strip('ABC')
            for i in range(4, 11):  # Use a minimum length of compression string to 4, going to have 9 comma at the most so at most 10 chars
                comp_str = test_str[-i:]
                score = len(comp_str) # * test_str.count(comp_str)
                candidates.append((score, comp_str))
            replacement = sorted(candidates, key=lambda x: x[0])[-1][1]
            commands[chr(current_replacement)] = replacement
            instructions = instructions.replace(replacement, chr(current_replacement))
            current_replacement += 1

        return instructions, commands


input_pipe, output_pipe = Pipe(), Pipe()
with open("day17.txt", "r") as f:
    computer = IntPuter(f.readline(), input_pipe, output_pipe)

computer.run()
droid = Day17Droid()
droid.load_grid(computer.output_pipe.data)
intersections = droid.find_intersections()
print("Part 1:", sum([x * y for x, y in intersections]))

output_pipe.clear()
computer.reset()

instructions, commands = droid.compress_commands()
print(instructions, commands)

for i in instructions:
    input_pipe.enqueue(ord(i))
input_pipe.enqueue(droid.UNKNOWN)
for command in ['A', 'B', 'C']:
    for i in commands[command]:
        input_pipe.enqueue(ord(i))
    input_pipe.enqueue(droid.UNKNOWN)


computer.set_loc(0, 2)
computer.run()

print(output_pipe.data)

print(droid.compress_commands())
