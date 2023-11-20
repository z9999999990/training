#!/usr/bin/env python
# coding = utf-8


def main():
    s = 600851475143

    for i in range(2, s):
        if s % i == 0:
            result = int(s / i)
            print((i), end=",")
            s = result


if __name__ == "__main__" :
    main()