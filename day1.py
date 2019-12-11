#!/usr/bin/env python3


def calc_fuel_mass(x):
    return x // 3 - 2


def calc_fuel_fuel(x):
    mass = calc_fuel_mass(x)
    if mass > 0:
        return calc_fuel_fuel(mass) + mass
    else:
        return 0


with open('day1.txt', 'r') as f:
    mass_list = [int(line) for line in f.readlines()]

print("Part 1:", sum(calc_fuel_mass(m) for m in mass_list))
print("Part 2:", sum(calc_fuel_fuel(m) for m in mass_list))
