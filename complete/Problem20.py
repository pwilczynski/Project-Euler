#!/usr/bin/python
# Copyright 2010 P. Wilczynski
# Project Euler
# Problem Number 20

import sys
import re
import math

"""
n! means n  (n  1)  ...  3  2  1

Find the sum of the digits in the number 100!

"""

def fact(n):
    n+=1
    result = 1
    for i in range(1, n):
        result = long(result*i)
    return result

        
def factorial(number):
    num_sum = 0
    f = math.factorial(number)
    print f
    f_string = str(f)
    for i in range(len(f_string)):
        num_sum += int(f_string[i])
    return num_sum
    
def home_fact(number):
    print "home!!!"
    num_sum = 0
    f = fact(number)
    print f
    f_string = str(f)
    for i in range(len(f_string)):
        num_sum += int(f_string[i])
    return num_sum
        
def main():
    number = long(sys.argv[1])
    print factorial(number)
    print home_fact(number)



if __name__ == '__main__':
  main()
