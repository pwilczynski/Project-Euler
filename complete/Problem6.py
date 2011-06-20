#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 5

import sys
import re

"""
2520 is the smallest number that can be divided 
by each of the numbers from 1 to 10 without any 
remainder.

What is the smallest positive number that is evenly
divisible by all of the numbers from 1 to 20?

"""


def dif_sumsq_sqsum(max):
  sq_sum = 0
  sum_sq = 0
  sum = 0
  max = max + 1
  for i in range(1,max):
    sq_sum += i*i
    print sq_sum
  for i in range(1, max):
    sum += i
    print sum
  sum_sq = sum*sum
  result = sum_sq - sq_sum

  return result
    

def main():
  number = long(sys.argv[1])
  print dif_sumsq_sqsum(number)

if __name__ == '__main__':
  main()
