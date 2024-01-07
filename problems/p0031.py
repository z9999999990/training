#/usr/bin/env python
# coding : utf-8

"""
Coin Sums
In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).
It is possible to make £2 in the following way:

1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
How many different ways can £2 be made using any number of coins?
"""

PID = 31
ANSWER = ''


def coin_sum(num, coins):
    
    sum_list = [0] * num
    sum_list[0] = 1

    for coin in coins:
        for now_num in range(coin, num+1):
            sum_list[now_num] +=sum_list[now_num - coin]
        
    return sum_list[num]


def solve() -> int:

    num = 200
    coins = [1, 2, 5, 10, 20, 50, 100, 200] 

    result = coin_sum(num, coins)

    return result