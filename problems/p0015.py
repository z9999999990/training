#!/usr/bin/env python
# coding: utf-8


"""
Lattice Paths
Starting in the top left corner of a 2 x 2grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

How many such routes are there through a 20 x 20 grid?

"""

PID = 15
ANSWER = 137846528820


def multi(num):
    up_sum = 1
    for i in range(1, num+1):
        up_sum = up_sum*i
    return up_sum

def solve() -> int:
    m = 20
    n = 20

    up_num = m + n
    down_num = m

    up_num = multi(m+n)
    down_num = multi(m) * multi(n)

    route_num = up_num / down_num

    return route_num
