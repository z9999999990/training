#!/usr/bin/env python
# coding = utf-8


def main():

    s2 = 0
    s3 = 0
    for i in range(1, 101):

        s1 = i*i
        s2 += s1

        s3 += i

    result = s3*s3 - s2
    print(result)


if __name__ == "__main__":
    main()
