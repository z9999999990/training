#!/usr/bin/env python
# coding : utf-8


"""
Goldbach's Other Conjecture
It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.
9=7+2 x 1^2
15 = 7  + 2 x 2^2
21 = 3  + 2 x 3^2
25 = 7  + 2 x 3^2
27 = 19 + 2 x 2^2
33= 31  + 2 x 1^2

It turns out that the conjecture was false.
What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
"""

PID = 46
ANSWER = ''


def is_prime(num) -> bool:
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
        
    return True


def solve() -> int:

    i = 9

    while True:
        if not is_prime(i):

            result = False
            for n in range(1, int(i**0.5)+1):
                p = i - 2 * (n**2)
                if is_prime(p):
                    result = True
                    break
            if not result:
                return i
        i += 2