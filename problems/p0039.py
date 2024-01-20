#!/usr/bin/env python
# coding : utf-8

"""
Integer Right Triangles
If p is the perimeter of a right angle triangle with integral length sides, {a, b, c}, there are exactly three solutions for p = 120.
{20, 48, 52}, {24, 45, 51}, {30, 40, 50}
For which value of p < 1000, is the number of solutions maximised?
"""

PID = 39
ANSWER = ''

def check_triangle(i) -> int:
    count = 0
    for a in range(1, i//2):
        for b in range(1, (i-a)//2):
            c = i - a - b
            if c^2 == a^2 + b^2:
                count += 1

    return count

def solve() -> int:
    num_old = 0
    max_i = 0
    for i in range(1, 1000):
        num_new = check_triangle(i)
        if num_new > num_old:
            num_old = num_new
            max_i = i

    return max_i