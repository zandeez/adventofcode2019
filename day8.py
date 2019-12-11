#!/usr/bin/env python3

w, h = 25, 6
size = w * h

with open('day8.txt', 'r') as f:
    d = [int(x) for x in f.readline().strip()]

layers = [
    d[x:x + size] for x in range(0, len(d), size)
]


def count_instances(enum, val):
    return len([x for x in enum if x == val])


best_layer = sorted(layers, key=lambda layer: count_instances(layer, 0))[0]

print("Part 1:", count_instances(best_layer, 1) * count_instances(best_layer, 2))

image = [0] * size
layers.reverse()
for layer in layers:
    for i, v in enumerate(layer):
        if v != 2:
            image[i] = v

print("Part 2:")

for y in range(h):
    for x in range(w):
        if image[y * w + x] == 1:
            print("O", end='')
        else:
            print(" ", end='')
    print()
