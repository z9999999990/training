#!/usr/bin/env python
# coding: utf-8


"""
Truncatable Primes
The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 
3797, 797, 97, and 7 . Similarly we can work from right to left: 3797, 379, 37 and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 
2, 3, 5,  and 7 are not considered to be truncatable primes.
"""

PID = 37
ANSWER = 748317

def is_primes(n) -> bool:
    
    if n < 2:
        return False

    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    
    return True

def panduan(num):
    str_num = str(num)
    for n in range(1, len(str_num)):
        r_cut = str_num[:-n]
        r_icut = int(r_cut)
        if not is_primes(r_icut):
            return False
            
        l_cut = str_num[n:]
        l_icut = int(l_cut)
        if not is_primes(l_icut):
            return False
    return True



def solve() -> int:
    sum = 0 
    count = 0
    num = 11

    while count < 11:

        if is_primes(num) and panduan(num):
            sum += num
            count += 1
        
        num += 2

    return sum