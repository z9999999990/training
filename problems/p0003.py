#!/usr/bin/env python
# coding = utf-8


"""
Largest Prime Factor
The prime factors of 13195 are 5, 7, 13 and 29.
What is the largest prime factor of the number 600851475143?
"""

PID = 3
ANSWER = 6857

def is_prime(n: int) -> bool:
    if n <= 2:
        return True
    
    i = 3

    while i * i <= n:
        if n % i == 0:
            return False
        
        i += 2
    return True

def solve() -> int:

    s = 600851475143
    i = 3

    while i * i <= s:
        if is_prime(i) and s % i == 0:
            s = s / i

        i += 2

    return s
