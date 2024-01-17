#!/usr/bin/env python3
# coding: utf-8



"""
Data of problem 22.
"""


def load():
    with open("data/p0022.txt", encoding="utf-8") as f:
        raw = f.read()

    items = raw.split(",")
    result = [x[1:-1] for x in items]   # remove quotes
    return result
