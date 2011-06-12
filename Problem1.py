#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 1

import sys
import re

"""

If we list all the natural numbers below 10 that are multiples of
3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.

"""


def sum_multiples(max):
  sum = 0
  for i in range(max):
    if (i%3 == 0 or i%5 == 0):
      sum += i
  print "The sum is: ", sum




def main():
  max = int(sys.argv[1])
  sum_multiples(max)



if __name__ == '__main__':
  main()
