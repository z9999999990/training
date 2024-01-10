#!/usr/bin/env python
# coding : utf-8

"""
Digit Cancelling Fractions
The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.
We shall consider fractions like, 30/50 = 3/ 5, to be trivial examples.
There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.
If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
"""

import math


PID = 33
ANSWER = 100


def solve() -> int :
    i_sum = 1
    j_sum = 1

    for i in range(10, 100):
        for j in range(i+1, 100):
            
            old_result = i / j 

            i_a = i // 10
            i_b = i % 10
            j_a = j // 10
            j_b = j % 10

            if i_b == j_a and j_b != 0: 
                if old_result == (i_a / j_b):
                    i_sum *= i_a
                    j_sum *= j_b
                    #print(i_a, j_b)

            if i_a == j_a and j_b != 0:
                if old_result == (i_b / j_b):
                    i_sum *= i_b
                    j_sum *= j_b
                    #print(i_b, j_b)

            if i_a == j_b and j_a != 0:
                if old_result == (i_b / j_a):
                    i_sum *= i_b
                    j_sum *= j_a

    max_s = math.gcd(i_sum, j_sum)
    result = int(j_sum / max_s)

    return result 
