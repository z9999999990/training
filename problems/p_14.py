#!/usr/bin/env python
# coding: utf-8

"""
Longest Collatz Sequence

The following iterative sequence is defined for the set of positive integers:
n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:
                13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.

It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
"""

PID = 14
ANSWER = ''

def len_count(n):
    p_list = [] 
    while n != 4:
        if n % 2 == 0:
            n = int(n / 2)
            p_list.append(n)
        elif n % 2 != 0:
            n = int(3 * n + 1)
            p_list.append(n)
    lenth = len(p_list) + 3
    
    return lenth


def solve() -> int :
    final_lenth = 0
    final_n = 0
    for n in range(1, 1000000):
        lenth = len_count(n)
        if lenth > final_lenth:
            final_lenth = lenth
            final_n = n
    
    return final_n