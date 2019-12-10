#!/usr/bin/env python3

planets = {}

with open('day6.txt', 'r') as f:
    for l in f.readlines():
        src, dst = l.strip().split(")")
        if src not in planets:
            planets[src] = []
        if dst not in planets:
            planets[dst] = []
        planets[src].append(dst)
        planets[dst].append(src)

total = 0
visited = set()
queue = [('COM', 0)]
while queue:
    src, dist = queue.pop(0)
    visited.add(src)
    dist += 1
    for p in [x for x in planets[src] if x not in visited]:
        total += dist
        queue.append((p, dist))


def bfs(start='COM', target=None):
    total = 0
    visited = set()
    queue = [(start, 0)]
    while queue:
        src, dist = queue.pop(0)
        visited.add(src)
        dist += 1
        for p in [x for x in planets[src] if x not in visited]:
            if p == target:
                return dist - 2
            total += dist
            queue.append((p, dist))

    return total


print("Part 1:", bfs())
print("Part 2:", bfs('YOU', 'SAN'))
