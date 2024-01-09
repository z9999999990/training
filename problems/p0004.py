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

def solve_slowly() -> int:
    list = []
    for i in range(100, 1000):
        for j in range(100, 1000):
            if reverse(i*j):
                list.append(i*j)
            
    s = max(list)
    return s

def is_Palindrome(n) -> bool:
    if n // 100000 != n % 10:
        return False
    elif n // 10000 % 10 != n % 100 // 10:
        return False
    elif n // 1000 % 10 != n % 1000 //100:
        return False
    else:
        return True

def solve_reverse() ->int:
    result = 0
    max_j = 0
    for i in range(999, 99, -1):
        for j in range(i, 99, -1):
                if i >= max_j:
                    n = i * j
                    if n > result and is_Palindrome(n):
                        max_j = j
                        result = n

    return result