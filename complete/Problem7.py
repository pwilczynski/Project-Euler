#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 7

import sys
import re

"""
By listing the first six prime numbers:
2, 3, 5, 7, 11, and 13, we can see that
the 6th prime is 13.

What is the 10001st prime number?
"""


def large_prime(number):
  count = 0
  number += 1
  n = 1
  while count < number:
      print count
      for x in range(2, n):
          if n % x == 0:
              break
      else:                                  
          # loop fell through without finding a factor
          count +=1
#          print n, 'is a prime'
      n +=1
  print count
  print n - 1, " is prime number  ", count
  
  
 

def main():
  number = long(sys.argv[1])
  large_prime(number)



if __name__ == '__main__':
  main()
