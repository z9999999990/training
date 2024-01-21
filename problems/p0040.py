#!/usr/bin/env python
# coding : utf-8


"""
Champernowne's Constant
An irrational decimal fraction is created by concatenating the positive integers:
0.123456789101112131415161718192021 ...
It can be seen that the 12th digit of the fractional part is 1.
If dn represents the nth digit of the fractional part, find the value of the following expression.
d1 X d10 X d100 X d1000 X d10000 X d100000 X d1000000
"""


PID = 40
ANSWER = ''


def solve_join() -> int :
    num_list = []
    for i in range(1, 1000000):
        num_list.append(str(i))

    num_str = "".join(num_list)

    indexs = [1, 10, 100, 1000, 10000, 100000, 1000000]
    number = 0
    result = 1

    for index in indexs:
        number = int(num_str[index - 1])
        result *= number

    return result

