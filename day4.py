#!/usr/bin/env python3

r = [171309, 643603]


def incr_only(num):
    prev = 0
    for i in [int(i) for i in str(num)]:
        if i < prev:
            return False
        prev = i
    return True


def contains_double(num):
    s = str(num)
    for patt in [str(i) for i in range(11, 121, 11)]:
        if patt in s:
            return True
    return False


def contains_double_exact(num):
    s = str(num)
    for x in range(0, 10):
        dbl = str(x * 11)
        trp = str(x * 111)
        if dbl in s and not trp in s:
            return True
    return False


# Part 1
l = [x for x in range(*r) if incr_only(x) and contains_double(x)]
print(len(l))

# Part 2
l = [x for x in range(*r) if incr_only(x) and contains_double_exact(x)]
print(len(l))
