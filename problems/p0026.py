#!/usr/bin/env python
# coding : utf-8

"""
Reciprocal Cycles
A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:
            
        1/2  = 0.5
        1/3  = 0.(3)
        1/4  = 0.25
        1/5  = 0.2
        1/6  = 0.1(6)
        1/7  = 0.(142857)
        1/8  = 0.125
        1/9  = 0.(1)
        1/10 = 0.1

Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.
Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.
"""

PID = 26
ANSWER = 983


def solve() -> int:

    max_length = 0

    for i in range(2, 1000):
        
        num_list = []
        num = 1 % i

        while num != 0 and num not in num_list:
            num_list.append(num)
            num = (num * 10) % i

        if len(num_list) > max_length:
            max_length = len(num_list)
            max_num = i
        
    return max_num