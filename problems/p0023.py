#/usr/bin/env python
# coding : utf-8

"""
Non-Abundant Sums
A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the sum of the proper divisors of 28 would be 
1 + 2 + 4 + 7 + 14 =28, which means that 28 is a perfect number.
A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum exceeds n.
As 12 is the smallest abundant number, 
1 + 2 + 3 + 4 + 6 =16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.
Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.
"""


PID = 23
ANSWER = 4179871


number = 28123
abundant_num = []


def p_sum(number):
    sum = 1
    num = number / 2
    for n in range(2, int(num+1)):
        if number % n == 0:
            sum += n
    return sum


def a(new_list):
    sum = 0
    for i in range(number+1):
        if i not in new_list:
            sum += i 
    return sum


def abu_sum(abundant_num):
    new_list = []
    for i in range(len(abundant_num)):
        for j in range(i, len(abundant_num)):
            result = abundant_num[i] + abundant_num[j]
            if result <= 28123:
                new_list.append(result)
                
    return new_list 


def solve() -> int :
    for num in range(12, number+1):
        result = p_sum(num)

        if result > num:
            abundant_num.append(num)


    new_list = abu_sum(abundant_num)
    sum = a(new_list)
    return sum


