#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 3

import sys
import re

"""
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
"""


def large_prime_factor(number):
  i = number
  end = False
  next = False
  while i>=0:
    if i!=0:
      rem = number%i
    if rem == 0:
      k = 1
      while k <= i :
        if (i%k == 0 and k != i and k != 1):
          break
        elif k==i:
          end = True
        k += 1
    if end:
      break
    i = i - 1
    
  large_prime = i
  print "The largest prime is: ", large_prime

def main():
  number = long(sys.argv[1])
  large_prime_factor(number)



if __name__ == '__main__':
  main()
