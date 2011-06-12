#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 10

import sys
import re

"""
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""


def large_prime(number):
  print "LARGE PRIME"
  sum = 0
  number += 1
  n = 2
  primes =[]
  while n < number:
      for x in primes:
          if n % x == 0:
              break
      else:                                  
          # loop fell through without finding a factor
          sum+=n
          print n
          primes.append(n)
#          print n, 'is a prime'
      if n <3:
          n +=1
      else:
          n+=2
  print sum
  

def other_prime(number):
  print "OTHER PRIME"
  sum = 0
  number += 1
  n = 2
  primes =[]
  while n < number:
      for x in primes:
          if n % x == 0:
              break
      else:                                  
          # loop fell through without finding a factor
          sum+=n
          print n
          primes.append(n)
#          print n, 'is a prime'
      n +=1
  print sum
  
  
 

def main():
  number = long(sys.argv[1])
  large_prime(number)
 # other_prime(number)



if __name__ == '__main__':
  main()
