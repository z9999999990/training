#!/usr/bin/env python
# coding = utf-8

"""

Summation of Primes

Find the sum of all the primes below two million.

"""

PID = 10
ANSWER = ''


def solve() -> int :
    list_p =[2,3,5]

    a = list_p[-1]
    sum = 0

    while a < 2000000:
        is_prime = True
        for p in list_p:
            if a % p == 0:
                is_prime = False
                continue
        if is_prime:
            list_p.append(a)
        a += 2

    for i in list_p:
        sum = sum + i
    return sum