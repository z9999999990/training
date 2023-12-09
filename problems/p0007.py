#!/usr/bin/env python
# coding = utf-8

"""
10001st Prime
By listing the first six prime numbers: 2,3,5,7,11,and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?

"""

PID = 7
ANSWER = 104743

def solve() -> int:
    p_list = [3,5,7,11,13,17,19]
    s = p_list[-1]

    while len(p_list) < 10001:
        is_prime = True
        for p in p_list:
            if s % p == 0:
                is_prime = False
                break
            if p * p > s:
                    break
        if is_prime:
            p_list.append(s)
        
        s += 2
        
    return p_list[-1]

