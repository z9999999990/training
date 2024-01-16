#!/usr/bin/env python
# coding: utf-8


"""
Circular Primes
The number, 197, is called a circular prime because all rotations of the digits: 
197, 971, and 719, are themselves prime.
There are thirteen such primes below 100: 2,3,5,7,11,13,17,31,37,71,73,79, and 97.
How many circular primes are there below one million?
"""


PID = 35
ANSWER = ''


def is_cprimes(i) -> bool:
    for num in range(2, int(i**0.5)+1):
        if i % num == 0:
            return False
    return True

def find_rotate(i):
    ro_list = []
    n_str = str(i)
    for l in range(1, len(n_str)):
        rotate_num = n_str[l:] + n_str[:l]
        ro_list.append(int(rotate_num))
    return ro_list

def solve() -> int:
    sum = 0
    for i in range(2, 1000000):
        result = True
        if is_cprimes(i):
            ro_list = find_rotate(i)
            for num in ro_list:
                if not is_cprimes(num):
                    result = False
                    break
            if result:
                sum += 1 
    
    return sum