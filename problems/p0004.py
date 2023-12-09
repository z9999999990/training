#!/usr/bin/env python
# coding = utf-8


"""
Largest Palindrome Product
A palindromic number reads the same both ways. The largest palindrome made from the product of two
2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""


PID = 4
ANSWER = 906609

    
def reverse(a):
    b = str(a)
    c = b[::-1]
    d = int(c)

    if a == d :
        return True
    else:
        return False

def solve() -> int:
    list = []
    for i in range(100, 1000):
        for j in range(100, 1000):
            if reverse(i*j):
                list.append(i*j)
            
    s = max(list)
    return s

