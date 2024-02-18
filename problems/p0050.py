#!/usr/bin/env python
# coding : utf-8


"""
Consecutive Prime Sum
The prime 41, can be written as the sum of six consecutive primes:
41=2+3+5+7+11+13.
This is the longest sum of consecutive primes that adds to a prime below one-hundred.
The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, 
and is equal to 953.

Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""

PID = 50
ANSWER = ''


def is_prime(num):
    if num < 2:
        return False
    
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
        
    return True

def solve() -> int :
    prime_sum = 2
    max_prime = 0
    i = 3

    while True:
        if is_prime(i):
            prime_sum += i
        
        i += 2
        if prime_sum < 1000 and is_prime(prime_sum):
            max_prime = prime_sum
        if prime_sum >= 1000:
            break


    
            
