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


def divisible(max):
  end = False
  test_num = max
  spec_num = 1
  print max
  i = max
  while not end:
    print test_num
    while i>0:
      print "    ", i, test_num
      if (test_num%i == 0 and i != 1):
        i = i - 1  
      elif (test_num%i == 0 and i == 1):
        spec_num=test_num
        end = True
        break
      else:
        test_num += max
        i = max
        break
  
  
  return spec_num
    

def main():
  number = long(sys.argv[1])
  print divisible(number)

if __name__ == '__main__':
  main()
