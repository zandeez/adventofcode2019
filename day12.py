#!/usr/bin/env python3
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations, count
from math import gcd
from typing import List


@dataclass
class Vector:
    x: int = 0
    y: int = 0
    z: int = 0

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)


@dataclass
class Planet:
    position: Vector = field(default_factory=Vector)
    velocity: Vector = field(default_factory=Vector)

    def apply_velocity(self):
        pass
        self.position += self.velocity
        pass

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


@dataclass
class System:
    planets: List[Planet] = field(default_factory=list)
    steps: int = 0

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
        self.steps += 1


def load_planets():
    r_planets = []
    with open("day12.txt", "r") as f:
        for li in f.readlines():
            li = li.strip("<>\r\n ")
            pos = Vector()
            items = li.split(",")
            for item in items:
                k, v = item.split("=")
                pos.__setattr__(k.strip(), int(v))
            r_planets.append(Planet(position=pos))
    return r_planets


planets = load_planets()
system = System(planets)

for x in range(100):
    system.step()

print(system)

print("Part 1:", system.energy())

system = load_planets()


while running:
    for i, planet in enumerate(running):
        e = ','.join([str(planet[x]) for x in ['x', 'y', 'z', 'vx', 'vy', 'vz']])
        if e in planet['states']:
            del running[i]
            planet['year'] = steps - planet['states'][e]
        planet['states'][e] = steps
    apply_gravity()
    apply_velocity()
    steps += 1


def lcm(denominators):
    return reduce(lambda a, b: a * b // gcd(a, b), denominators)


print("Part 2:", lcm(p['year'] for p in planets))
