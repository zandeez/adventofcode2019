#!/usr/bin/env python3
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations, count
from math import gcd
from typing import List, Dict

def lcm(denominators):
    return reduce(lambda a, b: a * b // gcd(a, b), denominators)

@dataclass
class HistoryScalar:
    history: Dict[int, int] = field(default_factory=dict, repr=False)
    period: int = field(default=0, repr=False)
    value: int = 0

    def store_history(self, steps):
        if self.value in self.history:
            self.period = steps - self.history[self.value]
        else:
            self.history[self.value] = steps

    def __set__(self, instance, value):
        instance.value = value

    def __iadd__(self, other):
        if isinstance(other, HistoryScalar):
            self.value += other.value
        else:
            self.value += other
        return self

    def __isub__(self, other):
        if isinstance(other, HistoryScalar):
            self.value -= other.value
        else:
            self.value -= other
        return self

    def __repr__(self):
        return str(self.value)

    def __abs__(self):
        return abs(self.value)

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __get__(self, instance, owner):
        return instance.value


@dataclass
class Vector:
    x: HistoryScalar = field(default_factory=HistoryScalar)
    y: HistoryScalar = field(default_factory=HistoryScalar)
    z: HistoryScalar = field(default_factory=HistoryScalar)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def store_history(self, steps):
        self.x.store_history(steps)
        self.y.store_history(steps)
        self.z.store_history(steps)

    def complete(self):
        return all(
            x.period for x in [self.x, self.y, self.z]
        )

    def lcm(self):
        return lcm([x.period for x in [self.x, self.y, self.z]])


@dataclass
class Planet:
    position: Vector = field(default_factory=Vector)
    velocity: Vector = field(default_factory=Vector)

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
        self.position.store_history(steps)
        self.velocity.store_history(steps)

    def complete(self):
        return all(
            v.complete() for v in [self.position, self.velocity]
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
        for p in planets:
            p.store_history(self.steps)
        self.steps += 1

    def complete(self):
        return all(
            p.complete() for p in planets
        )


def load_planets():
    r_planets = []
    with open("day12.txt", "r") as f:
        for li in f.readlines():
            li = li.strip("<>\r\n ")
            pos = Vector()
            items = li.split(",")
            for item in items:
                k, v = item.split("=")
                pos.__getattribute__(k.strip()).value = int(v)
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





print("Part 2:", lcm([x.position.lcm() for x in system.planets]))
