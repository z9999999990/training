#!/usr/bin/env python
# coding : utf-8

"""
Factorial digit sum
n! means n x (n-1) x ... x 3 x 2 x 1.
For example, 10! = 10 x 9 x ... x 3 x 2 x 1 = 3628800, and the sum of the digits in the number 10! is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.
Find the sum of the digits in the number 100!.
"""

PID = 20
ANSWER = 648

num = 100

def solve() -> int :
    i = 1
    sum = 1
    result = 0
    while i <= num:
        sum = i * sum
        i += 1

    for s in str(sum):
        result = int(s) + result

    return result