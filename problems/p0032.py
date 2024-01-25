#!/usr/bin/env python
# coding : utf-8

"""
Pandigital Products
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once;
for example, the 5-digit number, 15234, is 1 through 5 pandigital.
The product 7254 is unusual, as the identity, 39 x 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.
Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
"""

PID = 32
ANSWER = 45228


def solve() -> int:

    numlist = ''
    sum = 0

    cj_list = []

    # 两组循环合并的，i是1位数的时候j是4位数，i是2位数的时候j是3位数，其余情况重复
    for i in range(1, 100):
        for j in range(100, 10000):
            cj = i * j
            
            numlist = str(i) + str(j) +str(cj)
            if '0' not in numlist and len(numlist) == 9:
                numlist_str = "".join(sorted(numlist))

                if cj not in cj_list and numlist_str == '123456789' :
                    sum += cj 
                    cj_list.append(cj)

            numlist = []

    return sum
