#!/usr/bin/env python
# coding: utf-8

def main():
    a = 1
    b = 2
    c = a + b
    sum = 0
    while c < 4000000:
        a = b
        b = c
        c = a + b 
        print(c, end=' ')

        if c % 2 == 0:
            sum = sum + c


    print('\n')
    print("偶数和：", sum+2)

if __name__ == "__main__" :
    main()