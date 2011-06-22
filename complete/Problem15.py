#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 15

import sys
import re
import math

#for each path, there will be 20 horizontal moves
#for each path, there will be 20 vertical moves
#thus, there will be 40 total moves for each path
#any down move is indistinguishable from down, side from side
#formula = (x+y)!/(x!y!)

def factorial(n):
    f = 1
    while (n > 0):
        f = f * n
        n = n - 1
    return f

def paths(x,y):
    n_path = factorial(x+y)
    n_path = n_path/factorial(x)
    n_path = n_path/factorial(y)
    return n_path


def main():
    x , y = int(sys.argv[1]), int( sys.argv[1])
    i = paths(x,y)
    print i


if __name__ == '__main__':
  main()
