#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import List, Tuple, Set, FrozenSet

Location = Tuple[int, int]


@dataclass(frozen=True)
class State:
    location: Location = (0, 0)
    keys: FrozenSet[str] = field(default_factory=frozenset)
    steps: int = field(default=0, compare=False)

    def next_locations(self):
        return [
            (self.location[0], self.location[1] - 1),
            (self.location[0] + 1, self.location[1]),
            (self.location[0], self.location[1] + 1),
            (self.location[0] - 1, self.location[1]),
        ]

    def next_states(self, dungeon):
        states = [
            State(location=x, steps=self.steps + 1, keys=frozenset(list(self.keys) + [dungeon[x[0]][x[1]].upper()])) for
            x in self.next_locations()
            if dungeon[x[0]][x[1]] == '.' or dungeon[x[0]][x[1]].islower() or (dungeon[x[0]][
                                                                                   x[1]] in self.keys and dungeon[x[0]][
                                                                                   x[1]].isupper())]
        return states


with open("day18.txt", "r") as f:
    dungeon: List[str] = f.readlines()

# Find start location:
initial: State = None
for y, line in enumerate(dungeon):
    try:
        x = line.index('@')
    except:
        pass
    else:
        initial = State(location=(x, y), keys=frozenset(['.']))

queue: List[State] = [initial]
visited: Set[State] = set(queue)
while queue:
    state = queue.pop(0)
    visited.add(state)
    queue.extend([s for s in state.next_states(dungeon) if s not in visited])
    print(state)
