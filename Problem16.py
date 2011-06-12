#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 16

import sys
import re
import math

"""
2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2^1000?
"""

def twoup(num):
    add = 0
    ret = math.pow(2,num)
    print "2 to the", num, "power is", ret
    ret = int(ret)
    str_ret = str(ret)
    print str_ret
    for letter in str_ret:
        add+=int(letter)
    print "the sum of the digits is", add
        
  

def main():
  num = int(sys.argv[1])
  twoup(num)



if __name__ == '__main__':
  main()
