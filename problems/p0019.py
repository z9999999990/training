#!/usr/bin/env python3
# coding: utf-8


"""
Counting Sundays
You are given the following information, but you may prefer to do some research for yourself.
1 Jan 1900 was a Monday.
Thirty days has September, April, June and November.
All the rest have thirty-one, Saving February alone, Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
"""

PID = 19
ANSWER = 171

Month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def leap_year(year): 
    if year % 4 == 0:
        if year % 100 == 0 and year % 400 == 0:
            return True
    


def solve() -> int:
    #从1900年开始计算
    days = 365
    sum = 0

    for year in range(1901, 2001):
        for month in (1, 13):
            if days % 7 == 6:
                sum += 1
            days = days + Month[month]
            if month == 2 and leap_year(year):
                days += 1

    return sum