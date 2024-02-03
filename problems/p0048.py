#!/usr/bin/env python
# coding: utf-8


"""
Self powers
The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
"""

PID = 48
ANSWER = 9110846700
    
def solve() -> int:

    sum = 0

    for i in range(1, 1001):
        
        sum += i ** i

    result = str(sum)[-10:]
    
    return result