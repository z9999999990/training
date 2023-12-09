#!/usr/bin/env python
# coding = utf-8


"""
Sum Square Difference
The sum of the squares of the first ten natural numbers is,
    1^2 + 2^2 + ... + 10^2 = 385

The square of the sum of the first ten natural numbers is,
    (1 + 2 + ... + 10)^2 = 55^2 = 3025

Hence the difference between the sum of the squares of the first ten natural numbers and the square
of the sum is 3025 - 385 = 2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and the
square of the sum.
"""


PID = 6
ANSWER = 25164150

def solve() -> int:

    s2 = 0
    s3 = 0
    for i in range(1, 101):

        s1 = i*i
        s2 += s1

        s3 += i

    result = s3*s3 - s2
    return result

