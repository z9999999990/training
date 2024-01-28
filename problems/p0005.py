#!/usr/bin/env python
# coding = utf-8


"""
Smallest Multiple
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
"""


PID = 5
ANSWER = 232792560

def is_multiple(num) -> bool:
    for i in range(3,21):
        if num % i == 0:
            continue
        else:
            return False

    return True

def solve() -> int:
    result = False
    num = 20
    while not result:

        result = is_multiple(num)
        if not result:
            num += 20

    return num
                
