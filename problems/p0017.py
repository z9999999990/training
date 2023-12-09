#!/usr/bin/eenv python
# coding: utf-8

"""
Number Letter CountsS
If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.
If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?

NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.

"""

PID = 17
ANSWER = 21124

def number_to_words(number):
    transfor_num = {
        1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
        6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
        11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
        16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty',
        30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty',
        90: 'ninety', 100: 'hundred', 1000: 'one thousand'
    }

    word = ''
    if number == 1000:
        word = transfor_num[1000]
        return word

    if number >= 100:
        word = transfor_num[number // 100] + ' ' + transfor_num[100] + ' '
        number = number % 100 
        if number > 0:
            word = word + 'and' + ' '
            
        
    if number > 0:
        if number in transfor_num:
            word = word +transfor_num[number]
        else:
            n_single = number % 10 
            word = word + transfor_num[(number // 10 )* 10] + '-' + transfor_num[n_single] + ' '
    return word

def solve() -> int:
    lenth = 0
    for number in range(1, 1001):

        result = number_to_words(number)

        for r in result:
            if r == ' ' or r == '-':
                continue
            else:
                lenth += 1
                
    return lenth