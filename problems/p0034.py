#!/usr/bin/env python
# coding: utf-8


"""
Digit Factorials
145 is a curious number, as 1! + 4! + 5! = 1 +24 +120 =145.
Find the sum of all numbers which are equal to the sum of the factorial of their digits.
Note: As 1! = 1 and 2! = 2 are not sums they are not included.
"""

import math

PID = 34
ANSWER = 40730

def is_factorial(n):
    sum = 0
    for i in str(n):
       sum += math.factorial(int(i))
    if sum == n:
        return True
    else:
        return False

def solve_naive() -> int:
    result = 0
    for num in range(10, 2540161):
        if is_factorial(num):
            result += num

    return result
    
def solve_list() -> int:
    result = 0
    factorial_list = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
    index = 0
    
    for num in range(10, 2540161):
        sum = 0
        for i in str(num):
            index = int(i)
            sum += factorial_list[index]
            if sum == num:
                result += num

    return result
