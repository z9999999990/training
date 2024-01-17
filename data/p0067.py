#!/usr/bin/env python3
# coding: utf-8


"""
Load data of problem 67 from file.
"""


def load():
    result = []
    with open("data/p0067.txt", encoding="utf-8") as f:
        for line in f:
            result.append([int(x) for x in line.split()])

    return result
