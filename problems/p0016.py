#!/usr/bin/env python
# coding: utf-8

"""
Power DSigit SumS
2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2^1000.

"""

PID = 16
ANSWER = 1366

def solve() -> int:
    sum = 2
    i = 2

    while i <= 1000:
        sum *= 2
        i += 1

    sum_list = str(sum)
    num_sum = 0
    
    for num in sum_list:
        num_sum = int(num) + num_sum

    return num_sum