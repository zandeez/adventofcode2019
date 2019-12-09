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

def contains_quad(num):
  s = str(num)
  for patt in [str(i) for i in range(1111, 11110, 1111)]:
    if patt in s:
      return True
  return False

def not_triple(num):
  s = str(num)
  for patt in [str(i) for i in range(111, 1110, 111)]:
    if patt in s:
      return False
  return True

l = []  
for i in range(r[0], r[1]):
  if incr_only(i) and (contains_quad(i) or (contains_double(i) and not_triple(i))):
    l.append(i)

print(l)
print(len(l))
