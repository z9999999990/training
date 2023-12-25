#!/usr/bin/env python
# coding : utf-8

"""
Names score
Using names.txt(right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand 
first names, begin by sorting it into alphabetical order. 
Then working out the alphabetical value for each name, multiply this value by its alphabetical position in 
the list to obtain a name score.
For example, when the list is sorted into alphabetical order, COLIN, which is worth 3+15+12+9+14 =53, 
is the 938 th name in the list. So, COLIN would obtain a score of 938 x 53 = 49714.
What is the total of all the name scores in the file?
"""

PID = 22
ANSWER = 871198282


def change(letter):
    total_value = 0
    for num in letter:
        value = ord(num) - ord('A') + 1
        total_value += value
    return total_value

def count(list):
    result = 0
    i = 1
    for l in list:
        value_sum = change(l)
        result += value_sum * i
        i += 1
    return result

def solve() -> int:
    
    with open('./0022_names.txt', 'r+', encoding='utf-8') as f:
        name_list = f.read().replace('"','').split(',')

    name_list = sorted(name_list)
    result = count(name_list)
    return result 