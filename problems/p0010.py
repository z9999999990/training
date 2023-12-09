#!/usr/bin/env python
# coding = utf-8

"""
Summation of Primes
Find the sum of all the primes below two million.

"""

PID = 10
ANSWER = 142913828922


def solve() -> int :
    list_p =[2, 3]

    a = list_p[-1]
    sum = 0

    while a < 2000000:
        is_prime = True
        for p in list_p:
            if a % p == 0:
                is_prime = False
                break
            if p * p > a:
                break
        if is_prime:
            sum = sum + a
            list_p.append(a)
    a += 2
    sum = sum + 2
    return sum