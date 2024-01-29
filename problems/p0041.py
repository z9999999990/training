#!/usr/bin/env python
# coding : utf-8

"""
Pandigital Prime
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit
pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?
"""

PID = 41
ANSWER = 7652413


from itertools import permutations

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
        
    return True

def solve() -> int:
    max_num = 0
    for i in range(9, 1, -1):
        digit = []
        for n in range(1, i+1):
            digit.append(str(n))
        digits =  "".join(digit)
        for p in permutations(digits):
            p_num = int("".join(p))
            result = is_prime(p_num)

            if result and p_num > max_num:
                max_num = p_num
                

    return max_num