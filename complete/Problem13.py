#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 13

import sys
import re

"""
Work out the first ten digits of the sum of the following one-hundred 50-digit numbers.

"""


def tendigits(filename):
  f = open(filename, 'r')
  sum = 0
  for line in f:
      print line
      sum += int(line)
  f.close()
  print "Completed analysis"
  print sum
  print sum[0:9]
  
  
  

def main():
  filename = (sys.argv[1])
  tendigits(filename)



if __name__ == '__main__':
  main()
