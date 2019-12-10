#!/usr/bin/env python3

dimensions = [25, 6]
size = dimensions[0] * dimensions[1]

with open('day8.txt', 'r') as f:
    d = [int(x) for x in f.readline().strip()]

layers = [
    d[x:x + size] for x in range(0, len(d), size)
]

best_layer = None
best_score = size
for layer in layers:
    zeros = len([x for x in layer if x == 0])
    if zeros < best_score:
        best_score = zeros
        best_layer = layer

print("Part 1:", len([x for x in best_layer if x == 1]) * len([x for x in best_layer if x == 2]))

image = [0]*size
layers.reverse()
for layer in layers:
    for i in range(0, size):
        if layer[i] != 2:
            image[i] = layer[i]

print("Part 2:")

for x in range(dimensions[1]):
    for y in range(dimensions[0]):
        if image[x*dimensions[0]+y] == 1:
            print("O", end='')
        else:
            print(" ", end='')
    print()

