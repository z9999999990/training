#!/usr/bin/env python
# coding : utf-8

"""
Amicable Numbers
Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a != b, then a and b are an amicable pair and each of a and b are called amicable numbers.
For example, the proper divisors of 220 are 1,2,4,5,10,11,20,22,44,55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1,2,4,71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.
"""

PID = 21
ANSWER = ''


def d_sum(num: int) -> int :
    i = 1
    sum = 0
    while i < num:
        if num % i == 0 :
            sum += i
        i += 1
    return sum


def solve() -> int:
    sum = 0
    num = 1
    result_list = []
    while num <= 10000:
        result = d_sum(num)
        
        if result not in result_list:
            if d_sum(result) == num and result != num:
                sum += result + num
                result_list.append(result)
                result_list.append(num)
        num += 1

    return sum