#!/usr/bin/env python
# coding = utf-8


"""
Largest Prime Factor
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143?
"""

PID = 3
ANSWER = 6857


def solve() -> int:

    s = 600851475143

    for i in range(2, s):
        if s % i == 0:
            result = int(s / i)
            print((i), end=",")
            s = result

    return s

