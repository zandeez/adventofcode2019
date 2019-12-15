#!/usr/bin/env python3
import asyncio
from dataclasses import dataclass, field
from math import inf
from typing import List, Tuple, Dict, Set

from inputer import IntPuter, Pipe

Location = Tuple[int, int]


@dataclass
class Droid:
    # Known locations and what can be found there
    grid: Dict[Location, int] = field(default_factory=dict)
    # Droid current location
    location: Location = (0, 0)
    # Oxygen Location
    oxygen_location: Location = (0, 0)
    # Pipe to receive output from IntPuter
    input_pipe: Pipe = field(default_factory=Pipe)
    # Pipe to send output to IntPuter
    output_pipe: Pipe = field(default_factory=Pipe)

    # Location type values
    UNKNOWN = -1
    WALL = 0
    EMPTY = 1
    OXY = 2

    # Direction values
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

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
            # South
            (location[0], location[1] + 1),
            # West
            (location[0] - 1, location[1]),
            # East
            (location[0] + 1, location[1]),
        ]

    async def map_area(self) -> None:
        """
        Depth-first search to map the entire area. Takes nothing, returns nothing, updates self.grid
        """
        # Current path stack for the current location
        stack: List[Location] = [self.location]
        # Set of seen nodes to prevent loops
        visited: Set[Location] = set(stack)

        # When stack is empty, there is nowhere else to go.
        while stack:
            # Find the next possible locations to try. These are adjacent locations that are not a wall that have not
            # already been visited. Locations are enumerated from 1 so that the move command is the enumerated index.
            candidates: List[Tuple[int, Location]] = [
                (d, l) for d, l in enumerate(self.next_locations(), 1) if
                l not in visited and self.grid.get(l, Droid.UNKNOWN) != Droid.WALL
            ]

            if candidates:
                # If we have a candidate location, try move to that location.
                move, next_location = candidates[0]
            else:
                # If we have no candidate locations, we must backtrack to find one. Go to the previous location and work
                # out which move command is required to get there.
                next_location = stack.pop()
                if self.location[0] != next_location[0]:
                    if self.location[0] > next_location[0]:
                        move = Droid.WEST
                    else:
                        move = Droid.EAST
                else:
                    if self.location[1] > next_location[1]:
                        move = Droid.NORTH
                    else:
                        move = Droid.SOUTH

            # Send the move command
            self.output_pipe.enqueue(move)
            # Wait for the response
            result: int = await self.input_pipe.dequeue()
            # Update the grid with the result
            self.grid[next_location] = result
            # If we've found the oxygen location, save that for later
            if result == Droid.OXY:
                self.oxygen_location = next_location
            # Add it to our set of visited locations
            visited.add(next_location)
            # Only update position if we've not hit a wall
            if result != Droid.WALL:
                # If we've not backtracked, add old location to stack
                if candidates:
                    stack.append(self.location)
                # Update our current location
                self.location = next_location

    def shortest_route(self, destination: Location, start: Location = (0, 0)):
        """
        Breadth-first search to find the shortest route between any two points, start location defaults to (0, 0) if not
        specified. map_area should be called before calling this method.
        """
        # List of locations to test and their current path distance
        queue: List[Tuple[Location, int]] = [(start, 0)]
        # Set of visited locations
        visited: Set[Location] = set(start)
        # Current distance that can be returned if no route is found (Part 2, floods the map and finds the longest
        # possible distance)
        distance: int = 0
        # Loop while we have nodes to consider queued
        while queue:
            # Get the next location from the queue
            next_location, distance = queue.pop(0)
            # If it is our target, return the distance
            if next_location == destination:
                return distance
            else:
                # Get the next possible states, these are adjacent locations that are not walls and haven't been
                # visited
                next_states = [x for x in self.next_locations(next_location) if
                               self.grid.get(x, Droid.UNKNOWN) != Droid.WALL and x not in visited]
                # Add the next state to the queue and visited state set
                queue.extend([(x, distance + 1) for x in next_states])
                visited.update(next_states)
        # If no route has been found, return last distance value (longest possible distance from origin).
        return distance


# Set up asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# Communication pipes
input_pipe, output_pipe = Pipe(), Pipe()

# Load IntPuter code
with open("day15.txt", "r") as f:
    computer = IntPuter(f.readline(), input_pipe, output_pipe)

# Create Droid instance
droid = Droid(input_pipe=output_pipe, output_pipe=input_pipe)
# Start computer
task = loop.create_task(computer.run_async())
# Run until mapping is complete
loop.run_until_complete(droid.map_area())
# Kill computer
task.cancel()

# Shorted route from Origin (0,0) to the oxygen location
print("Part 1:", droid.shortest_route(droid.oxygen_location, (0, 0)))
# Longest distance possible from oxygen location. Forces exhaustive BFS by setting an impossible destination.
print("Part 2:", droid.shortest_route((inf, inf), droid.oxygen_location))
