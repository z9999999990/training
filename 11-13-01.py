#!/usr/bin/env python
# coding: utf-8

def main():
    a = 0

    for i in range(1,1000):
        if i % 3 == 0:
            a = a + i
        elif i % 5 == 0:
            a = a + i
            
    print(a)


if __name__ == "__main__" :
    main()
