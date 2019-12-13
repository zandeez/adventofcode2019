#!/usr/bin/env python3
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations
from math import gcd
from typing import List, Set


def lcm(denominators):
    return reduce(lambda a, b: a * b // gcd(a, b), denominators)


@dataclass
class Vector:
    x: int = 0
    y: int = 0
    z: int = 0

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)


@dataclass
class Planet:
    position: Vector = field(default_factory=Vector)
    velocity: Vector = field(default_factory=Vector)

    x_set: Set = field(default_factory=set)
    y_set: Set = field(default_factory=set)
    z_set: Set = field(default_factory=set)

    x_cycle: bool = False
    y_cycle: bool = False
    z_cycle: bool = False

    def apply_velocity(self):
        self.position += self.velocity

    def energy(self) -> int:
        return self.position.energy() * self.velocity.energy()

    def gravity(self, other):
        if self.position.x > other.position.x:
            self.velocity.x -= 1
            other.velocity.x += 1
        elif self.position.x < other.position.x:
            self.velocity.x += 1
            other.velocity.x -= 1

        if self.position.y > other.position.y:
            self.velocity.y -= 1
            other.velocity.y += 1
        elif self.position.y < other.position.y:
            self.velocity.y += 1
            other.velocity.y -= 1

        if self.position.z > other.position.z:
            self.velocity.z -= 1
            other.velocity.z += 1
        elif self.position.z < other.position.z:
            self.velocity.z += 1
            other.velocity.z -= 1
        pass

    def store_history(self, steps: int):
        x_state = (self.position.x, self.velocity.x)
        if x_state in self.x_set:
            self.x_cycle = True
        else:
            self.x_set.add(x_state)

        y_state = (self.position.y, self.velocity.y)
        if y_state in self.y_set:
            self.y_cycle = True
        else:
            self.y_set.add(y_state)

        z_state = (self.position.z, self.velocity.z)
        if z_state in self.z_set:
            self.z_cycle = True
        else:
            self.z_set.add(z_state)

    def complete(self):
        return all(
            [self.x_cycle, self.y_cycle, self.z_cycle]
        )

    def lcm(self):
        return lcm(
            [len(x)-1 for x in [self.x_set, self.y_set, self.z_set]]
        )


@dataclass
class System:
    planets: List[Planet] = field(default_factory=list)
    steps: int = field(default=0, repr=False)

    def apply_gravity(self):
        for p1, p2 in combinations(self.planets, 2):
            p1.gravity(p2)

    def apply_velocity(self):
        for p in self.planets:
            p.apply_velocity()

    def energy(self):
        return sum(p.energy() for p in self.planets)

    def step(self):
        self.apply_gravity()
        self.apply_velocity()
        for p in self.planets:
            p.store_history(self.steps)
        self.steps += 1

    def complete(self):
        return all(
            p.complete() for p in self.planets
        )

    def lcm(self):
        return lcm([
            p.lcm() for p in self.planets
        ])


def load_planets():
    r_planets = []
    with open("day12.txt", "r") as f:
        for li in f.readlines():
            li = li.strip("<>\r\n ")
            pos = Vector()
            items = li.split(",")
            for item in items:
                k, v = item.split("=")
                setattr(pos, k.strip(), int(v))
            r_planets.append(Planet(position=pos))
    return r_planets


planets = load_planets()
system = System(planets)

for x in range(1000):
    system.step()

print(system)

print("Part 1:", system.energy())

planets = load_planets()
system = System(planets)

while not system.complete():
    system.step()

print("Part 2:", "FUCK THIS")
