#!/usr/bin/env python
# coding: utf-8

a = 0

for i in range(1,1000):
    if i % 3 == 0:
        a = a + i
    elif i % 5 == 0:
        a = a + i
    else :
        i += 1

print(a)